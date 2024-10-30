# Setup
See [README.md](README.md) for installation.

# Introducing a new API call.
> **_NOTE:_** we will use `get_task_info` as an example below.

1. Add a new file at `audithub_client/api`, implementing the rpc. Use the convention `api_...` for naming the RPC function. Make the function accept at most two arguments. 
    1. The first should be an AuditHubContext, with the needed information to contact AuditHub successfully.
    2. The second, if required, should be a data class encapsulating all the RPC parameters (both URL and body)

    e.g.: Add file `api/get_task_info.py` introducing the type for the input:
    ```Python
    GetTaskInfoArgs:
        organization_id: int
        task_id: int
    ``` 
    and then implement the API function:
    ```Python
    def api_get_task_info(context: AuditHubContext, input: GetTaskInfoArgs):
        ...
    ```

2. Add a new file at `audithub_client/scripts`, implementing the CLI for the RPC. Declare all parameters the user can provide at the command line.
    e.g: Add file `scripts/get_task_info.py` and implement:
    ```Python
    @app.command
    def get_task_info(
        section: Optional[str] = None,
        *,
        organization_id: OrganizationIdType,
        task_id: Annotated[int, Parameter(name=["--task-id", "-t"])],
        output: OutputType = "json",
        verify: bool = False,
        rpc_context: AuditHubContextType,
    ):
        ...
    ```
    Import the RPC from the api module, invoke it, and use any extra command line arguments to format the output or implement extra functionality for the CLI execution. e.g.:
    1. `section`, `output`, to allow the user to select what to output and its format,
    2. `verify`, to examine a task's output and produce the correct exit code to signal success or failure.

3. At `audithub_client/__main__.py`, add a line to include the function from the script. e.g.:
    ```Python
    from .scripts.get_task_info import get_task_info  # noqa
    ```
