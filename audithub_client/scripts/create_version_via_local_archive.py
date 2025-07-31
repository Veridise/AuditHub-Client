import logging
from os import SEEK_END, walk
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import Annotated, Optional
from zipfile import ZIP_DEFLATED, ZipFile

from cyclopts import Group, Parameter, validators
from cyclopts.types import ExistingDirectory, ExistingFile

from ..api.create_version_via_local_archive import (
    CreateVersionViaLocalArchiveArgs,
    api_create_version_via_local_archive,
)
from ..library.invocation_common import (
    AuditHubContextType,
    OrganizationIdType,
    ProjectIdType,
    app,
)

logger = logging.getLogger(__name__)


EXCLUDED_DIRECTORIES: set[str] = {".git"}
EXCLUDED_FILE_NAME_PREFIXES: list[str] = []
EXCLUDED_FILE_EXTENSIONS: list[str] = []


def add_folder_to_zip(
    archive: ZipFile,
    source_folder: Path,
    excluded_directories: set[str],
    excluded_file_name_prefixes: list[str],
    excluded_file_extensions: list[str],
):
    for root, _dirs, files in walk(source_folder):
        current_root = Path(root)
        if current_root.name in excluded_directories:
            continue
        if any(
            map(
                lambda p: str(p) in excluded_directories,
                current_root.relative_to(source_folder).parents,
            )
        ):
            continue
        for file_name in files:
            if any(map(file_name.startswith, excluded_file_name_prefixes)):
                continue
            current_file = current_root / file_name
            if any(map(current_file.suffix.__eq__, excluded_file_extensions)):
                continue
            current_zip_file_name = str(current_file.relative_to(source_folder))
            logger.info("Adding %s", current_zip_file_name)
            try:
                archive.write(current_file, current_zip_file_name)
            except Exception as ex:
                logger.warning(
                    f"Failed to add file {current_file} to the archive", exc_info=ex
                )


source = Group(
    "Source for obtaining version data (choose exactly one)",
    default_parameter=Parameter(negative=""),  # Disable "--no-" flags
    validator=validators.LimitedChoice(min=1),  # Mutually Exclusive Options
)


@app.command
def create_version_via_local_archive(
    *,
    organization_id: OrganizationIdType,
    project_id: ProjectIdType,
    name: str,
    archive_path: Annotated[Optional[ExistingFile], Parameter(group=source)] = None,
    source_folder: Annotated[
        Optional[ExistingDirectory], Parameter(group=source)
    ] = None,
    excluded_directories: Annotated[
        set[str],
        Parameter(env_var="AUDITHUB_ZIP_EXCLUDED_DIRECTORIES", consume_multiple=True),
    ] = EXCLUDED_DIRECTORIES,
    excluded_file_name_prefixes: Annotated[
        list[str],
        Parameter(
            env_var="AUDITHUB_ZIP_EXCLUDED_FILE_EXTENSIONS", consume_multiple=True
        ),
    ] = EXCLUDED_FILE_EXTENSIONS,
    excluded_file_extensions: Annotated[
        list[str],
        Parameter(
            env_var="AUDITHUB_ZIP_EXCLUDED_FILE_EXTENSIONS", consume_multiple=True
        ),
    ] = EXCLUDED_FILE_EXTENSIONS,
    rpc_context: AuditHubContextType,
):
    """
    Create a new version for a project by uploading either a preexisting local .zip archive,
    or creating a .zip archive on the fly from a source folder.
    Only one of --archive-path or --source-folder can be specified.

    Parameters
    ----------
    name:
        The name of the new version to be created
    archive_path:
        The local path to the version .zip archive. If specified, it must exist.
    source_folder:
        The local path to a folder with the sources for the version. If specified, it will be zipped on the fly and submitted.
    """
    try:
        logger.debug("Starting...")
        rpc_input = CreateVersionViaLocalArchiveArgs(
            organization_id=organization_id, project_id=project_id, name=name
        )

        if source_folder is not None:
            logger.info("Creating a .zip file on the fly...")
            with SpooledTemporaryFile() as tmp_file:
                with ZipFile(tmp_file, "w", ZIP_DEFLATED) as archive:
                    add_folder_to_zip(
                        archive,
                        source_folder,
                        excluded_directories,
                        excluded_file_name_prefixes,
                        excluded_file_extensions,
                    )
                tmp_file.seek(0, SEEK_END)
                file_size = tmp_file.tell()
                tmp_file.seek(0)

                logger.info(
                    "Posting dynamically generated version archive of size %d bytes",
                    file_size,
                )

                ret = api_create_version_via_local_archive(
                    rpc_context, rpc_input, tmp_file
                )
        else:
            assert archive_path is not None
            file_size = archive_path.stat().st_size
            logger.info(
                "Posting version %s with archive %s of size %d bytes",
                name,
                archive_path,
                file_size,
            )
            with archive_path.open("rb") as fp:
                ret = api_create_version_via_local_archive(rpc_context, rpc_input, fp)

        logger.debug("New version response %d", ret)
        print(ret["id"])
        logger.debug("Finished.")
    except Exception as ex:
        logger.error("Error %s", str(ex), exc_info=ex)
