from pathlib import Path
import numpy as np
from tifffile import imread
from typing import Union


class Spot2Cell:
    def __init__(self, spots, mask):
        self.spots = spots
        self.mask = mask

        # Index mask file at the spot table coordinate to get the cell id of each spot (0 for background)
        spots = self.mask[self.spots[:, 0], self.spots[:, 1]]

        # Get the unique cell ids and their counts
        self.cell_ids, self.counts = np.unique(spots, return_counts=True)

        # Get the number of background spots
        self.background_spots = self.counts[1:]

        # Get the non-zero cell ids and their counts
        self.cell_ids = self.cell_ids[1:]
        self.counts = self.counts[1:]

        # Create a zero numpy array the size of the number of cell ids in the mask
        self.cell_spots = np.zeros((self.mask.max(), 2), dtype=np.uint32)

        # Fill the first column of cell_counts with consecutive cell ids
        self.cell_spots[:, 0] = np.arange(1, self.mask.max() + 1)

        # Assign the counts to the corresponding cell ids
        self.cell_spots[self.cell_ids - 1, 1] = self.counts

    def save(self, output_path: Union[str, None, Path] = None) -> None:
        """
        Save the cell assigned spots to a csv file with a header row.
        """
        np.savetxt(output_path, self.cell_spots, delimiter=',', header='CellID,spot_count', comments='', fmt='%d')

    def __setattr__(self, key: str, value: object) -> None:
        """
        Sets class attributes, it validates the input type for spots and mask.
        """
        if key == 'spots':
            if isinstance(value, np.ndarray):
                self.__dict__[key] = value
            elif isinstance(value, str) or isinstance(value, Path):
                self.__dict__[key] = np.genfromtxt(value, delimiter=',', skip_header=1, dtype=np.uint32)
            elif value is None:
                self.__dict__[key] = value
            else:
                raise TypeError("Spot table must be of type np.array, string or Path.")

        elif key == 'mask':
            if isinstance(value, np.ndarray):
                self.__dict__[key] = value
            elif isinstance(value, str) or isinstance(value, Path):
                self.__dict__[key] = imread(value)
            elif value is None:
                self.__dict__[key] = value
            else:
                raise TypeError("Mask must be of type np.array, string or Path.")

        else:
            self.__dict__[key] = value
