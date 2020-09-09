#!/usr/bin/env python3
import argparse
import json
from typing import List, Optional, Iterable
from dataclasses import dataclass
import itertools

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
UNDERLINED = "\x1b[4m"
BRRED = "\x1b[31m"
RED = "\x1b[91m"
BRGREEN = "\x1b[32m"
GREEN = "\x1b[92m"
BRYELLOW = "\x1b[33m"
CYAN = "\x1b[96m"
RESET_FG = "\x1b[39m"

YES = f"{GREEN}Yes{RESET_FG}"
NO = f" {RED}No{RESET_FG}"


@dataclass
class License:
    reference: str
    isDeprecatedLicenseId: bool
    detailsUrl: str
    referenceNumber: str
    name: str
    licenseId: str
    seeAlso: List[str]
    isOsiApproved: bool
    isFsfLibre: Optional[bool] = None

    def pretty(self) -> str:
        # id (name)
        # deprecated
        # url
        # see also
        # is OSI approved
        # is fsf libre
        ret = f"{BOLD}{BRYELLOW if self.isDeprecatedLicenseId else BRGREEN}{self.licenseId}{RESET} ({self.name})"
        if self.isDeprecatedLicenseId:
            ret += f" {BRRED}{BOLD}(deprecated){RESET}"

        ret += f"\n{BOLD}OSI approved?{RESET} " + (YES if self.isOsiApproved else NO)

        if self.isFsfLibre is not None:
            ret += f"\n{BOLD}FSF Libre?{RESET}    " + (YES if self.isFsfLibre else NO)

        ret += f"\n{BOLD}See also:{RESET}" + "".join(
            f"\n • {CYAN}{UNDERLINED}{url}{RESET}"
            for url in itertools.chain(
                (f"https://spdx.org/licenses/{self.licenseId}",), self.seeAlso
            )
        )
        return ret


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="spdx tool helper")
    parser.add_argument("LICENSE_ID")
    return parser


def main():
    args = argparser().parse_args()
    with open("@licenseJson@") as f:
        data = json.load(f)
        expectedId = args.LICENSE_ID
        license = License(
            **next(l for l in data["licenses"] if l["licenseId"] == expectedId)
        )
        print(license.pretty())


if __name__ == "__main__":
    main()
