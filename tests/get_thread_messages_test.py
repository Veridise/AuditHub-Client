import os
import unittest
from dataclasses import asdict
from audithub_client.api.get_version_comments import (
    api_get_version_comments,
    GetVersionCommentsArgs,
)
from audithub_client.library.context import AuditHubContext
from audithub_client.library.json_dump import dump_dict


class TestOrCaInvocation(unittest.TestCase):

    def test_get(self):
        args = GetVersionCommentsArgs(
            organization_id=os.environ.get("AUDITHUB_ORGANIZATION_ID"),
            project_id=os.environ.get("AUDITHUB_PROJECT_ID"),
            version_id=os.environ.get("AUDITHUB_VERSION_ID"),
            thread_id=os.environ.get("AUDITHUB_THREAD_ID"),
        )
        rpc_context = AuditHubContext(
            base_url=os.environ.get("AUDITHUB_BASE_URL"),
            oidc_configuration_url=os.environ.get("AUDITHUB_OIDC_CONFIGURATION_URL"),
            oidc_client_id=os.environ.get("AUDITHUB_OIDC_CLIENT_ID"),
            oidc_client_secret=os.environ.get("AUDITHUB_OIDC_CLIENT_SECRET"),
        )
        result = api_get_version_comments(context=rpc_context, input=args)
        dump_dict(result)


if __name__ == "__main__":
    unittest.main()
