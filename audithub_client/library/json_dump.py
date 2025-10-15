from json import dumps
from pprint import pprint
from typing import Annotated, Any, Literal

from cyclopts import Parameter
from tabulate import tabulate

OutputType = Annotated[
    Literal["raw", "json", "json-pretty", "pprint", "list", "table", "none"],
    Parameter(
        help="""\
The output format. Options are: 'raw': Python print(), 'json': single-line JSON, 'json-pretty': multi-line JSON, 'pprint': Python pprint(), 'list': list element per line, 'table': tabular view, 'none': omit output completely.
"""
    ),
]


def dump_dict(document: Any, section: str | None = None, output: OutputType = "json"):
    if output == "none":
        return
    if section == "sections":
        document = sorted(document.keys())
    elif section:
        document = document[section]

    if output == "raw":
        print(document)
    elif output == "pprint":
        # if isinstance(document, list):
        #     print(*document, sep="\n")
        # else:
        pprint(document, indent=2)
    elif output == "list":
        if isinstance(document, list):
            for e in document:
                print(e)
        else:
            pprint(document, indent=2)
    elif output == "json":
        print(dumps(document))
    elif output == "json-pretty":
        print(dumps(document, indent=2))
    elif output == "table":
        print(tabulate(document, headers="keys"))
    else:
        print(document)
