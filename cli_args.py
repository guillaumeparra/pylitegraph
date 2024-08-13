import argparse
import enum
import os
from typing import Optional
import options


class EnumAction(argparse.Action):
    """
    Argparse action for handling Enums
    """
    def __init__(self, **kwargs):
        # Pop off the type value
        enum_type = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum_type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        choices = tuple(e.value for e in enum_type)
        kwargs.setdefault("choices", choices)
        kwargs.setdefault("metavar", f"[{','.join(list(choices))}]")

        super(EnumAction, self).__init__(**kwargs)

        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        value = self._enum(values)
        setattr(namespace, self.dest, value)


parser = argparse.ArgumentParser()

parser.add_argument("--listen", type=str, default="127.0.0.1", metavar="IP", nargs="?", const="0.0.0.0", help="Specify the IP address to listen on (default: 127.0.0.1). If --listen is provided without an argument, it defaults to 0.0.0.0. (listens on all)")
parser.add_argument("--port", type=int, default=8188, help="Set the listen port.")
parser.add_argument("--tls-keyfile", type=str, help="Path to TLS (SSL) key file. Enables TLS, makes app accessible at https://... requires --tls-certfile to function")
parser.add_argument("--tls-certfile", type=str, help="Path to TLS (SSL) certificate file. Enables TLS, makes app accessible at https://... requires --tls-keyfile to function")
parser.add_argument("--enable-cors-header", type=str, default=None, metavar="ORIGIN", nargs="?", const="*", help="Enable CORS (Cross-Origin Resource Sharing) with optional origin or allow all with default '*'.")
parser.add_argument("--max-upload-size", type=float, default=100, help="Set the maximum upload size in MB.")

parser.add_argument("--auto-launch", action="store_true", help="Automatically launch ComfyUI in the default browser.")
parser.add_argument("--disable-auto-launch", action="store_true", help="Disable auto launching the browser.")

parser.add_argument("--disable-xformers", action="store_true", help="Disable xformers.")

upcast = parser.add_mutually_exclusive_group()
upcast.add_argument("--force-upcast-attention", action="store_true", help="Force enable attention upcasting, please report if it fixes black images.")
upcast.add_argument("--dont-upcast-attention", action="store_true", help="Disable all upcasting of attention. Should be unnecessary except for debugging.")

parser.add_argument("--dont-print-server", action="store_true", help="Don't print server output.")
parser.add_argument("--quick-test-for-ci", action="store_true", help="Quick test for CI.")
parser.add_argument("--windows-standalone-build", action="store_true", help="Windows standalone build: Enable convenient things that most people using the standalone windows build will probably enjoy (like auto opening the page on startup).")
parser.add_argument("--disable-all-custom-nodes", action="store_true", help="Disable loading all custom nodes.")

parser.add_argument("--multi-user", action="store_true", help="Enables per-user storage.")

parser.add_argument("--verbose", action="store_true", help="Enables more debug prints.")

# The default built-in provider hosted under web/
DEFAULT_VERSION_STRING = ""

parser.add_argument(
    "--front-end-version",
    type=str,
    default=DEFAULT_VERSION_STRING,
    help="""
    Specifies the version of the frontend to be used. This command needs internet connectivity to query and
    download available frontend implementations from GitHub releases.

    The version string should be in the format of:
    [repoOwner]/[repoName]@[version]
    where version is one of: "latest" or a valid version number (e.g. "1.0.0")
    """,
)

def is_valid_directory(path: Optional[str]) -> Optional[str]:
    """Validate if the given path is a directory."""
    if path is None:
        return None

    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} is not a valid directory.")
    return path

parser.add_argument(
    "--front-end-root",
    type=is_valid_directory,
    default=None,
    help="The local filesystem path to the directory where the frontend is located. Overrides --front-end-version.",
)

if options.args_parsing:
    args = parser.parse_args()
else:
    args = parser.parse_args([])

if args.windows_standalone_build:
    args.auto_launch = True

if args.disable_auto_launch:
    args.auto_launch = False

import logging
logging_level = logging.INFO
if args.verbose:
    logging_level = logging.DEBUG

logging.basicConfig(format="%(message)s", level=logging_level)
