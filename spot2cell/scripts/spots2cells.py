import os
import argparse
from spot2cell import __version__
from spot2cell import Spot2Cell
import pathlib
from pathlib import Path
if os.name == 'nt':
    pathlib.PosixPath = pathlib.WindowsPath


def get_args():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Assign spots to cells.')
    parser.add_argument('-s', '--spots', type=str, help='Path to the spot table csv file.')
    parser.add_argument('-m', '--mask', type=str, help='Path to the cell mask tif file.')
    parser.add_argument('-o', '--output', type=str, help='Path to the output csv file.')
    parser.add_argument('--version', action='version', version=f'{__version__}')
    args = parser.parse_args()

    # Standardize paths
    # Convert WindowsPath to PosixPath
    args.spots = Path(args.spots).resolve()
    args.mask = Path(args.mask).resolve()
    args.output = Path(args.output).resolve()

    return args


def main():
    # Get the arguments
    args = get_args()

    # Create an instance of the Spot2Cell class.
    spots = Spot2Cell(args.spots, args.mask)

    # Save the assigned spots to a csv file.
    spots.save(args.output)


if __name__ == '__main__':
    main()
