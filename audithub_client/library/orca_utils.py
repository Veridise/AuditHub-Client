from typing import Optional

from ..api.start_orca_task import FuzzingBlacklistEntry


def restructure_fuzzing_blacklist(
    original: Optional[list[str]],
) -> Optional[list[FuzzingBlacklistEntry]]:
    """
    The goal of this function is to restructure a list of strings
    in the form of "contract.function" to a fuzzing blacklist of separate
    contract and function fields.
    Validation includes disallowing empty contact and/or function names
    """
    if not original:
        return None
    ret: list[FuzzingBlacklistEntry] = []
    for entry in original:
        tokens: list[str] = entry.split(".")
        if len(tokens) != 2 or not tokens[0] or not tokens[1]:
            raise RuntimeError(f"Invalid fuzzing blacklist entry: {entry}")
        ret.append(FuzzingBlacklistEntry(contract=tokens[0], function=tokens[1]))
    return ret
