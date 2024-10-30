from typing import Annotated

from cyclopts import App, Parameter

from .context import AuditHubContext

app = App(
    help="""\
This is the Veridise AuditHub CLI client, that allows access to AuditHub via its REST API. 
When you have Veridise AuditHub credentials, you can use this tool to, 
e.g., create new versions for projects, launch Veridise tools, monitor their progress, and obtain the results.
This tool can be used in CI/CD pipelines to assist in verifying new versions of projects. 
""",
)


AuditHubContextType = Annotated[AuditHubContext, Parameter(parse=False)]

OrganizationIdType = Annotated[
    int,
    Parameter(
        name=["--organization-id", "-o"],
        env_var="AUDITHUB_ORGANIZATION_ID",
        help="The organization id.",
    ),
]
ProjectIdType = Annotated[
    int,
    Parameter(
        name=["--project-id", "-p"],
        env_var="AUDITHUB_PROJECT_ID",
        help="The project id, inside the selected organization.",
    ),
]
VersionIdType = Annotated[
    int,
    Parameter(
        name=["--version-id", "-v"],
        env_var="AUDITHUB_VERSION_ID",
        help="The version id, inside the selected project.",
    ),
]
