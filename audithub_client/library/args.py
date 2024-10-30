import argparse
import logging
from dataclasses import fields
from os import getenv
from sys import stderr
from typing import Callable, Optional

from .context import AuditHubContext


def from_env_or_required(env_var, help):
    env_value = getenv(env_var)
    common = {"help": f"{help} (env: {env_var})"}
    if env_value:
        return {"default": env_value} | common
    else:
        return {"required": True} | common


def from_env_or_default(env_var, default, help):
    return {"default": getenv(env_var, default), "help": f"{help} (env: {env_var})"}


def saas_args(extra_args: Optional[Callable[[argparse.ArgumentParser], None]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        **from_env_or_required("AUDITHUB_BASE_URL", help="AuditHub base URL"),
    )
    parser.add_argument(
        "--oidc-configuration-url",
        **from_env_or_required(
            "AUDITHUB_OIDC_CONFIGURATION_URL", help="AuditHub OIDC configuration URL"
        ),
    )
    parser.add_argument(
        "--oidc-client-id",
        **from_env_or_required(
            "AUDITHUB_OIDC_CLIENT_ID", help="AuditHub OIDC client id"
        ),
    )
    parser.add_argument(
        "--oidc-client-secret",
        **from_env_or_required(
            "AUDITHUB_OIDC_CLIENT_SECRET",
            help="AuditHub OIDC client secret",
        ),
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=logging.getLevelNamesMapping().keys(),
        **from_env_or_default(
            "AUDITHUB_LOG_LEVEL", logging.INFO, help="Log level (INFO)"
        ),
    )
    if extra_args:
        extra_args(parser)
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        # format="%(asctime)s.%(msecs)03d %(filename)s%(name)s %(levelname)s %(message)s",  # cspell:disable-line
        format="%(asctime)s %(levelname)s %(message)s",  # cspell:disable-line
        datefmt="%H:%M:%S",
        stream=stderr,
    )
    return args, AuditHubContext(
        **{
            k: v
            for (k, v) in vars(args).items()
            if k in map(lambda e: e.name, fields(AuditHubContext))
        }
    )
