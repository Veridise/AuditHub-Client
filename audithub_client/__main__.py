from typing import Annotated, Literal

from cyclopts import Group, Parameter

from audithub_client.library.logging_level import set_logging_level

from .library.invocation_common import app

from .scripts.create_version_via_local_archive import (  # noqa
    create_version_via_local_archive,
)
from .scripts.create_version_via_url import create_version_via_url  # noqa
from .scripts.download_artifact import download_artifact  # noqa
from .scripts.get_configuration import get_configuration  # noqa
from .scripts.get_my_organizations import get_my_organizations  # noqa
from .scripts.get_my_profile import get_my_profile  # noqa
from .scripts.get_task_archive import get_task_archive  # noqa
from .scripts.get_task_artifact import get_task_artifact  # noqa
from .scripts.get_task_info import get_task_info  # noqa
from .scripts.get_task_logs import get_task_logs  # noqa
from .scripts.get_users import get_users  # noqa
from .scripts.get_version_archive import get_version_archive  # noqa
from .scripts.monitor_task import monitor_task  # noqa
from .scripts.start_orca_task import start_orca_task  # noqa
from .scripts.start_picus_v2_task import start_picus_v2_task  # noqa
from .scripts.start_vanguard_task import (  # noqa
    start_defi_vanguard_task,
    start_defi_vanguard_v2_task,
    start_zk_vanguard_task,
)


app.meta.group_parameters = Group("Global Parameters", sort_key=99)


@app.meta.default
def meta(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    log_level: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        Parameter(
            name=["--log-level", "-l"],
            help="Log level",
            env_var="AUDITHUB_LOG_LEVEL",
        ),
    ] = "INFO",
):
    set_logging_level(log_level)

    command, bound, _ignored = app.parse_args(tokens)

    return command(*bound.args, **bound.kwargs)


def main():
    app.meta()


if __name__ == "__main__":
    main()
