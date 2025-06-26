import logging
import sys
from typing import Annotated, Literal

from cyclopts import Group, Parameter

from .library.context import AuditHubContext
from .library.invocation_common import app

app.meta.group_parameters = Group("Global Parameters")
from .scripts.create_version_via_local_archive import (  # noqa
    create_version_via_local_archive,
)
from .scripts.create_version_via_url import create_version_via_url  # noqa
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


@app.meta.default
def meta(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    base_url: Annotated[
        str, Parameter(env_var="AUDITHUB_BASE_URL", help="AuditHub base URL")
    ],
    oidc_configuration_url: Annotated[
        str,
        Parameter(
            env_var="AUDITHUB_OIDC_CONFIGURATION_URL",
            help="AuditHub OpenID Connect configuration URL",
        ),
    ],
    oidc_client_id: Annotated[
        str,
        Parameter(
            env_var="AUDITHUB_OIDC_CLIENT_ID", help="AuditHub OpenID Connect client id"
        ),
    ],
    oidc_client_secret: Annotated[
        str,
        Parameter(
            env_var="AUDITHUB_OIDC_CLIENT_SECRET",
            help="AuditHub OpenID Connect client secret. Please note that this is confidential information.",
        ),
    ],
    log_level: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        Parameter(
            name=["--log-level", "-l"],
            help="Log level",
            env_var="AUDITHUB_LOG_LEVEL",
        ),
    ] = "INFO",
):
    logging.basicConfig(
        level=log_level,
        # format="%(asctime)s.%(msecs)03d %(filename)s%(name)s %(levelname)s %(message)s",  # cspell:disable-line
        format="%(asctime)s %(levelname)s %(message)s",  # cspell:disable-line
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)

    command, bound, _ignored = app.parse_args(tokens)
    # When this script runs with no args, help_print is automatically invoked
    # Only in this situation however, it fails with: "TypeError: App.help_print() got an unexpected keyword argument 'rpc_context'"
    # By only, I mean it does not fail when invoked with "--help".
    # So let's treat it differently
    if command == app.help_print:
        return command(*bound.args, **bound.kwargs)
    return command(
        *bound.args,
        **bound.kwargs,
        rpc_context=AuditHubContext(
            base_url=base_url,
            oidc_configuration_url=oidc_configuration_url,
            oidc_client_id=oidc_client_id,
            oidc_client_secret=oidc_client_secret,
        ),
    )


def main():
    app.meta()


if __name__ == "__main__":
    main()
