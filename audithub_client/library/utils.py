from argparse import Namespace
from dataclasses import asdict, fields
from inspect import currentframe


def func():
    return currentframe().f_back.f_code.co_name


def parent_func():
    return currentframe().f_back.f_back.f_code.co_name


def get_dict_of_fields_except(data_class_object, exceptions: set[str]) -> dict:
    return {
        k: v
        for (k, v) in asdict(data_class_object).items()
        if k not in exceptions and v is not None
    }


def instantiate_from_args(data_class: type, args: Namespace):
    class_fields = set(map(lambda e: e.name, fields(data_class)))
    return data_class(**{k: v for (k, v) in vars(args).items() if k in class_fields})


def asdict_exclude_none(dc) -> dict:
    return asdict(dc, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
