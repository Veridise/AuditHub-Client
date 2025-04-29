This is the AuditHub client, a Python module that allows programmatic access to Veridise AuditHub via its REST API.

# Installing
- Allocate and activate a venv, e.g., `python -m venv .venv && source .venv/bin/activate`
- Make sure you have `poetry` installed. If it cannot be found globally, you can install it in the local venv with `pip install poetry`
- Run `poetry install`

# Configuring
All commands support configuration via command line arguments. Additionally, some arguments can also be specified as environment variables.
The required arguments for any API call are the following (the name inside the parenthesis is the corresponding environment variable name):
- `--base-url` (`AUDITHUB_BASE_URL`): The base url to use for API calls. The environments are as follows:
  - `dev`: https://audithub.dev.veridise.tools/api/v1
  - `production`: https://audithub.veridise.com/api/v1
- `--oidc-configuration-url` (`AUDITHUB_OIDC_CONFIGURATION_URL`): OpenID Connect configuration URL. The values per environment are as follows:
  - `dev`: https://keycloak.dev.veridise.tools/auth/realms/veridise/.well-known/openid-configuration
  - `production`: https://sso.veridise.com/auth/realms/veridise/.well-known/openid-configuration
- `--oidc-client-id` (`AUDITHUB_OIDC_CLIENT_ID`): The OIDC client id (to be supplied by Veridise upon request)
- `--oidc-client-secret` (`AUDITHUB_OIDC_CLIENT_SECRET`): The OIDC client secret (to be supplied by Veridise upon request). 

Note: use `ah --help` to see the global arguments, applicable to all commands.
Note: any logging output produced by the `ah` script is directed to stderr, so that output 

**Important**: please note that the `client_id` and `client_secret` pair should be considered sensitive information, as anyone with access to these can trigger AuditHub actions that account towards the usage limits of the organization that was issued these credentials.

We suggest to set these arguments in the environment for ease of use. 
One approach is to use [direnv](https://direnv.net), for which we provide two sample files: `envrc-sample-dev` and `envrc-sample-production`. 
If you would like to use this utility, copy one of the samples corresponding to your target environment as `.envrc`, edit `.envrc` to fill in your credentials, and you can then use the below command line utilities.

# Command line usage
We offer a global `ah` script, that offers commands that make API calls. 
Use `ah --help` to list all supported commands, as well as the global options that apply to all commands.
To get help for a specific command, use `ah command --help`. For example: `ah get-task-info --help`.

Any option that can be set via an environment variable, also lists the corresponding environment variable name in the help text.
To set a list option via an environment variable, use JSON notation. e.g.: `export LIST_OPTION='["value 1", "value 2"]'`
To set a list option via the command line, either repeat the same option multiple times, or separate the list elements via space. e.g.:
```shell
ah cmd --list-option "value 1" --list-option "value 2"
# or
ah cmd --list-option "value 1" "value 2"
```

# Verifying connectivity

Once you receive your credentials, enable them in the shell environment and run: `ah get-my-profile`.

This should output information about your user profile in AuditHub, and can help verify the validity of your credentials.


# API Usage
If you would like to use this module as a library, utilized by your own Python code, you can import the corresponding function from the API call you are interested in. 
e.g., to invoke the `get_my_profile` function programmatically, you can do the following:
```python
from audithub_client.api.get_my_profile import api_get_my_profile
from audithub_client.library.context import AuditHubContext
from os import getenv

# Fill in the corresponding values below
rpc_context = AuditHubContext(
    base_url=getenv("AUDITHUB_BASE_URL"), 
    oidc_configuration_url=getenv("AUDITHUB_OIDC_CONFIGURATION_URL"), 
    oidc_client_id=getenv("AUDITHUB_OIDC_CLIENT_ID"), 
    oidc_client_secret=getenv("AUDITHUB_OIDC_CLIENT_SECRET")
)
print(api_get_my_profile(rpc_context))
```

# Script reference
For a current script reference, please use `ah --help`. 
Some interesting commands are the following:
  - `create-version-via-local-archive`  Create a new version for a project by uploading a local .zip archive, or creating one on the fly from a local folder.
  - `create-version-via-url`            Create a new version for a project by asking AuditHub to either download an archive or clone a Git repository.
  - `get-configuration`                 Get global AuditHub configuration.
  - `get-task-info`                     Get detailed task information.
  - `monitor-task`                      Monitor a task's progress. Will exit with an exit status of 1 if the task did not complete successfully.
  - `start-defi-vanguard-task`          Start a Vanguard (static analysis) task for a specific version of a project.
  - `start-picus-v2-task`               Start a Picus V2 (Rust version) task for a module of a specific version of a project.

> **Note:** all `ah start-...` commands support a `--wait` option that automatically invokes `ah monitor-task` on the newly started task, to wait for it to finish and exit with 0 on success or non-zero on failure.

> **Note:** The .zip files, created on the fly by `create-version-via-local-archive` with the `--source-folder` option, automatically exclude any `.git` folder as well as empty directories. If this does not match your requirements, you can still create a `.zip` archive outside `ah` and use that to upload a version with the same command but the `--archive-path` option.

# Example usage to verify a new version with Picus

Assuming that:
  1. a new version .zip archive exists at `new_version.zip`, for a new version to be named `new_version`
  2. all `AUDITHUB_...` env vars for accessing the API are properly set
  3. `AUDITHUB_ORGANIZATION_ID` and `AUDITHUB_PROJECT_ID` are also properly set, pointing to a specific organization and project

you can run the following as a script to upload the new version to AuditHub and start a Picus task named `new_task_name` to examine a specific file in it (`some/file.picus` in the example below):
```bash
#!/usr/bin/env bash
set -e
version_id=$(ah create-version-via-local-archive --name "new_version" --archive-path new_version.zip)
task_id=$(ah start-picus-v2-task --version-id $version_id --source some/file.picus)
ah monitor-task --task-id $task_id
ah get-task-info --task-id $task_id --section findings_counters --verify
```
If the above exits with a 0 exit code, then all steps completed successfully and there were no issues found in the examined code.

# Obtaining the logs

Additionally, if you want to download the output of the tool, or any step of the task execution, you can invoke:
`ah get-task-logs --task-id $task_id --step-code run-picus`

For a list of valid step codes that you can use for a task, you can use:
`ah get-task-info --task-id $task_id --section steps --output table`

Or, to get a parsable list:
`ah get-task-info --task-id $task_id --section steps --output json | jq -r '. [].code'`

With this, you can preserve all logs locally:
`for step in $(ah get-task-info --task-id $task_id --section steps --output json | jq -r '. [].code'); do ah get-task-logs --task-id $task_id --step-code $step > $step.log; done`

# Building a container image
Use `make image` to just build the `latest` tag.

Use `make image-versioned` to build an image tagger with both `latest` and the current version number of this module, as stored in `pyproject.toml`

Finally, use `make push` to push latest and `make push-versioned` to push the image tagger with the current version.

As a side note, for `docker build --platform=linux/amd64,linux/arm64 ...` to work, the machine's container runtime needs to support multi-platform builds. Specifically for Docker, this requires switching from the "classic" image store to the containerd image store as outlined [here](https://docs.docker.com/build/building/multi-platform/).
For Docker Desktop, you can set the "Use containerd for pulling and storing images" option in the user interface as described [here](https://docs.docker.com/desktop/features/containerd/). 
