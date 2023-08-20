#!/usr/bin/python

import os
import csv
import argparse
import pathlib
from rich.console import Console
from rich.table import Table


def sortFun(e):
    """Returns column to be used for sorting"""

    return e["size"]


def cli() -> list:
    """Returns list of files greater than a size set by the user
    Args:
        minimum (int): Minimum file size in MBs.
        base (str): Base directory to begin search.
        file (str): File to save results

    Returns:
        result (list): List of dict

    Raises:
        Pending: Raises an exception.
    """

    # TODO move file size functionality to its own function and add arg for the feature
    # TODO add file search functionality
    # TODO add ability to include multiple base drives and directories

    drive = pathlib.Path.home().drive + "\\"

    parser = argparse.ArgumentParser(
        prog="FSAS",
        description="File size and search.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Yet another implementation of a filesystem file size and search cli app.""",
    )

    default_size = 250
    parser.add_argument(
        "-m",
        "--minimum",
        type=int,
        required=False,
        default=default_size,
        help=f"Minimum file size to include in results. Default ({default_size} MBs)",
    )
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

    file_list = []
    total_directories = 0
    total_files = 0
    console_progress = Console()
    with console_progress.status("Pending...") as status:
        for root, dirs, files in os.walk(args.base):
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
                    if (file_stats.st_size / (1024 * 1024)) > args.minimum:
                        file_list.append(
                            {
                                "size": file_stats.st_size / (1024 * 1024),
                                "location": f"{root_final}{file}",
                            }
                        )
                # TODO take appropriate action based on exception type
                except Exception as e:
                    print(e.__doc__)
    file_list.sort(reverse=True, key=sortFun)

    # TODO move print table to function
    # TODO add arg for user to determine whether they want output to screen or not
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Size (MBs)", justify="right", no_wrap=True)
    table.add_column("File", justify="left")
    for record in file_list:
        table.add_row(f"{record['size']:,.4f}", record["location"])
    console = Console()
    console.print(table)

    try:
        if args.file is not None:
            header = ["size", "location"]
            with open(args.file, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
                writer.writerows(file_list)
    except Exception as e:
        print(f"Error: {e.__doc__}")
        return 1


if __name__ == "__main__":
    cli()
