import logging
import sys


class LevelFormatter(logging.Formatter):
    def __init__(self, formats, default_fmt=None):
        super().__init__()
        self.formats = formats
        self.default_fmt = default_fmt or "%(levelname)s: %(message)s"

    def format(self, record):
        fmt = self.formats.get(record.levelno, self.default_fmt)
        formatter = logging.Formatter(fmt)
        return formatter.format(record)


def set_logging_level(log_level: str):
    # Leave all levels except DEBUG "simple", without outputting the module name.
    # At debug level, also show the module name that produces the log message.
    default_log_format = "%(asctime)s %(levelname)s %(message)s"
    debug_log_format = "%(asctime)s %(levelname)s %(name)s %(message)s"

    # Setup logging as usual
    logging.basicConfig(
        level=log_level,
        format=default_log_format,
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )
    # Now modify the root logger
    root_logger = logging.getLogger()
    handler = root_logger.handlers[0]  # basicConfig creates one handler by default
    handler.setFormatter(
        LevelFormatter(
            {logging.DEBUG: debug_log_format}, default_fmt=default_log_format
        )
    )

    # For these modules, raise the log level to reduce noise
    for module in ["httpx", "httpcore"]:
        module_logger = logging.getLogger(module)
        module_logger.setLevel(logging.WARNING)
