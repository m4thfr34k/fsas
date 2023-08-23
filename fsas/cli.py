#!/usr/bin/python

import os
import csv
import argparse
import pathlib
from rich.console import Console
from rich.table import Table
from typing import List


def sortFun(e):
    """Returns column to be used for sorting"""

    return e["size"]


def find_large_files(args: argparse.Namespace) -> List:
    """Returns list of files greater than a size set by the user.

    Args:
        args (Namespace): Expecting base(str) and minimum(int)

    Returns:
        List: List of dict containing the size and file's full path and name
    """

    base = args.base
    minimum = args.minimum
    file_list = []
    total_directories = 0
    total_files = 0
    console_progress = Console()
    with console_progress.status("Pending...") as status:
        for root, dirs, files in os.walk(base):
            total_directories += 1
            for file in files:
                try:
                    total_files += 1
                    status.update(
                        f"Reviewed | Directories: {total_directories:,} - Files: {total_files:,}"
                    )
                    # TODO update so root/path is correct for any filesystem
                    # Need to use standard package for root+file contruction
                    root_final = root if (root[-1] == "\\") else (f"{root}\\")
                    file_stats = os.stat(f"{root_final}{file}")
                    if (file_stats.st_size / (1024 * 1024)) > minimum:
                        file_list.append(
                            {
                                "size": file_stats.st_size / (1024 * 1024),
                                "location": f"{root_final}{file}",
                            }
                        )
                # TODO take appropriate action based on exception type
                except Exception as e:
                    print(e.__doc__)
                    return e
    return file_list


def find_files(args: argparse.Namespace) -> List:
    """Returns list of files matching a pattern set by the user.

    Args:
        args (Namespace): Expecting base(str) and match(str)

    Returns:
        List: List of files, with full path, that match the given search string(match).
    """

    # TODO Implementation
    return []


def cli() -> List:
    # TODO add file search functionality
    # TODO add ability to include multiple base drives and directories
    # TODO add tests

    drive = pathlib.Path.home().drive + "\\"

    parser = argparse.ArgumentParser(
        prog="FSAS",
        description="File size and search.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Yet another implementation of a filesystem file size and search cli app.""",
    )

    subparsers = parser.add_subparsers(required=True)
    size_search_parser = subparsers.add_parser(
        "size", help="Returns list of files greater than a size set by the user."
    )
    size_search_parser.set_defaults(func=find_large_files)

    default_size = 250
    size_search_parser.add_argument(
        "-m",
        "--minimum",
        type=int,
        required=False,
        default=default_size,
        help=f"Minimum file size to include in results. Default ({default_size} MBs)",
    )

    file_search_parser = subparsers.add_parser(
        "search", help="Returns list of files matching a pattern set by the user."
    )
    file_search_parser.add_argument(
        "-m",
        "--match",
        type=str,
        required=False,
        default="*",
        help=f"Search string for file matching. Default (*)",
    )
    file_search_parser.set_defaults(func=find_files)

    parser.add_argument(
        "-b",
        "--base",
        type=str,
        required=False,
        default=drive,
        help=f"Base directory where search will begin. Default ({drive})",
    )
    parser.add_argument(
        "-f", "--file", type=str, required=False, help="Output file for saving results."
    )

    args = parser.parse_args()
    file_list = args.func(args)

    if type(file_list) is Exception:
        print(f"Error: {e.__doc__}")
        return 1

    if type(file_list) is not list or len(file_list) == 0:
        print("No results")
        return 0

    file_list.sort(reverse=True, key=sortFun)

    # TODO move print table to function
    # TODO add arg for user to determine whether they want output to screen or not
    table = Table(show_header=True, header_style="bold magenta")
    headers = list(file_list[0].keys())
    for col in headers:
        table.add_column(col, justify="center", no_wrap=True)
    for record in file_list:
        str_values = [str(x) for x in list(record.values())]
        table.add_row(*(str_values))
    console = Console()
    console.print(table)

    try:
        if args.file is not None:
            with open(args.file, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(file_list)
    except Exception as e:
        print(f"Error: {e.__doc__}")
        return 1


if __name__ == "__main__":
    cli()
