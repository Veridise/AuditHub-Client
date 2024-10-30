#!/bin/sh
MODULE="audithub_client"
echo "isort.." && isort $MODULE && echo "mypy..." && mypy $MODULE && echo "ruff..." && ruff check $MODULE

# On mypy errors about missing type information, you may need to run:
# mypy --install-types --non-interactive
