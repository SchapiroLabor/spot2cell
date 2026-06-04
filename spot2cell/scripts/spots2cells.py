import argparse
import os
import pathlib
from math import log
from pathlib import Path
from re import L
from typing import Dict, List, Optional, Sequence, Tuple

from spot2cell import Spot2Cell, __version__, logger

if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath


def CLI() -> argparse.ArgumentParser:
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="This scripts assigns a list of spots to the objects in an instance mask."
    )
    parser.add_argument(
        "-s",
        "--spots",
        type=Path,
        help="Path to the spot table file.",
    )
    parser.add_argument(
        "-m",
        "--mask",
        type=Path,
        help="Path to the isntance mask file.",
    )
    parser.add_argument(
        "-x",
        "--x-col",
        type=int,
        default=0,
        help="Column index of the x coordinate in the spots table [default: 0].",
    )
    parser.add_argument(
        "-y",
        "--y-col",
        type=int,
        default=1,
        help="Column index of the y coordinate in the spots table [default: 1].",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to the output csv file.",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging.")
    parser.add_argument("--version", action="version", version=f"{__version__}")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    # Get CLI arguments
    parser = CLI()
    args = parser.parse_args(argv)

    # Resolves the paths to absolute paths
    args.spots = args.spots.resolve()
    args.mask = args.mask.resolve()
    args.output = args.output.resolve()

    # Set logger
    LOGGER = logger.set_logger(log_level="debug" if args.verbose else "info")
    LOGGER.info(f"spot2cell version: {__version__}")
    LOGGER.info(f"Reading mask from: {args.mask}")
    LOGGER.info(f"Reading spots from: {args.spots}")

    try:
        # Create an instance of the Spot2Cell class.
        LOGGER.info(f"Creating Spot2Cell instance")
        Spots = Spot2Cell(
            args.spots,
            args.mask,
            x_col=args.x_col,
            y_col=args.y_col,
            logger=LOGGER,
        )

        # Save the assigned spots to a csv file.
        LOGGER.info(f"Writing assigned spots to: {args.output}")
        Spots.save(args.output)

        return 0

    except Exception as e:
        print(f"spot2cells exit with an error: {e}")
        return 1


if __name__ == "__main__":
    main()
