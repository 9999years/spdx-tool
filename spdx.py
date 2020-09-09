#!/usr/bin/env python3
import subprocess
import os
from os import path
import argparse
import sys

__version__ = "@version@"

RESET = "\x1b[0m"
UNDERLINED = "\x1b[4m"
BRGREEN = "\x1b[32m"
BRRED = "\x1b[31m"


def error(message: str):
    print(f"{BRRED}[spdx] error: {message}{RESET}", file=sys.stderr)
    sys.exit(1)


def get_license_id() -> str:
    with open("@shortLicenseList@", "rb") as f:
        proc = subprocess.run(
            [
                "fzf",
                "--tiebreak=begin",
                "--min-height=15",
                "--height=50%",
                "--prompt=SPDX License ID > ",
                "--preview-window=up:6:wrap",
                f"--preview=@infoHelper@ {{1}}",
            ],
            input=f.read(),
            stdout=subprocess.PIPE,
        )
    out = proc.stdout.decode("utf-8")
    if out:
        return out.split()[0]
    else:
        return ""


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Writes LICENSE.txt files from SPDX expressions.
See https://spdx.org/licenses/ for a full list of licenses.

Uses version @spdxVersion@ of the SPDX license data from
https://github.com/spdx/license-list-data/
""",
    )
    parser.add_argument("--version", action="version", version="%(prog)s @version@")
    parser.add_argument(
        "-o",
        "--output",
        default="LICENSE.txt",
        help="Output filename; defaults to LICENSE.txt",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite LICENSE.txt if it exists"
    )
    parser.add_argument(
        "LICENSE_ID",
        default="",
        nargs="?",
        help="SPDX License ID; if omitted, an interactive picker will open",
    )
    return parser


def main():
    args = argparser().parse_args()

    if path.exists(args.output) and not args.force:
        error(
            f"{args.output} already exists and --force not given; either use --force to overwrite the file or --output to provide an alternate filename"
        )

    if args.LICENSE_ID:
        license_id = args.LICENSE_ID
    else:
        license_id = get_license_id()

    if not license_id:
        error("no license selected")

    with open(args.output, "wb") as output, open(
        f"@licenseTextDir@/{license_id}.txt", "rb"
    ) as license:
        output.write(license.read())

    print(
        f"{BRGREEN}{license_id} license text copied to {UNDERLINED}{args.output}{RESET}"
    )


if __name__ == "__main__":
    main()
