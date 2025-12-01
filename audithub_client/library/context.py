from dataclasses import dataclass
from typing import Annotated

from cyclopts import Group, Parameter

audithub_context_group = Group("AuditHub connection parameters", sort_key=10)


@dataclass
class AuditHubContext:
    base_url: Annotated[
        str,
        Parameter(
            env_var="AUDITHUB_BASE_URL",
            help="AuditHub base URL",
            group=audithub_context_group,
        ),
    ]
    oidc_configuration_url: Annotated[
        str,
        Parameter(
            env_var="AUDITHUB_OIDC_CONFIGURATION_URL",
            help="AuditHub OpenID Connect configuration URL",
            group=audithub_context_group,
        ),
    ]
    oidc_client_id: Annotated[
        str,
        Parameter(
            env_var="AUDITHUB_OIDC_CLIENT_ID",
            help="AuditHub OpenID Connect client id",
            group=audithub_context_group,
        ),
    ]
    oidc_client_secret: Annotated[
        str,
        Parameter(
            env_var="AUDITHUB_OIDC_CLIENT_SECRET",
            help="AuditHub OpenID Connect client secret. Please note that this is confidential information.",
            group=audithub_context_group,
        ),
    ]
