#!/usr/bin/env python3
import argparse
import json
from typing import List, Optional, Iterable
from dataclasses import dataclass


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


def pad(s: str, width: int) -> str:
    delta = width - len(s)
    if delta > 0:
        return s + " " * delta
    else:
        return s


def table(data: List[List[str]], sep: str = " ") -> str:
    if not data:
        return ""

    col_widths = [-1] * len(data[0])

    for row in data:
        for width, (i, cell) in zip(col_widths, enumerate(row[:-1])):
            if len(cell) > width:
                col_widths[i] = len(cell)

    return "\n".join(
        sep.join(
            pad(cell, width) if width != -1 else cell
            for cell, width in zip(row, col_widths)
        )
        for row in data
    )


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="spdx tool build script")
    parser.add_argument("LICENSE_DATA")
    return parser


def main():
    args = argparser().parse_args()
    with open(args.LICENSE_DATA) as f:
        data = json.load(f)
        licenses = [License(**l) for l in data["licenses"]]
        table_data = [
            [l.licenseId, l.name] for l in licenses if not l.isDeprecatedLicenseId
        ]
        print(table(table_data))


if __name__ == "__main__":
    main()
