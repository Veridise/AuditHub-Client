This is a command-line client for AuditHub, a comprehensive security platform for web3.

High-level information about what AuditHub offers can be found here: https://docs.audithub.dev/

The production API can be found here: https://audithub.veridise.com/api/v1/docs

For information about the code structure and general developer guidelines read README.md and "Developer Instructions.md".

This CLI must NEVER give access to any admin APIs.

Always ensure the following:
1. New code is consistent with existing code conventions.
2. Run `mypy .` on the root of the repo and ensure there are no type errors.