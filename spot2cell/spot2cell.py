from pathlib import Path
from syslog import LOG_INFO
from typing import Union

import numpy as np
from tifffile import imread

from . import logger


class Spot2Cell:
    """
    Assign spots to cells in a mask. The mask is a binary image where each cell is represented by a unique integer
    value. The spots are a table with the x and y coordinates of each spot. The spots are assigned to the cells by
    indexing the mask at the spot coordinates.

    Attributes:
    spots: Table with the x and y coordinates of each spot.
    mask: Binary image where each cell is represented by a unique integer value.
    labels: Unique mask labels (ie. Cell IDs).
    counts: Number of spots in each cell.
    background_spots: Number of spots in the background.
    cell_spots: Table with the cell id and the number of spots in each cell.
    labeled_spots: Table with the cell id and the number of spots in each cell.

    Methods:
    assign_spots: Assign spots to cells in the mask.
    save: Save the cell assigned spots to a csv file with a header row.
    """

    def __init__(
        self,
        spots: Union[str, Path, np.ndarray],
        mask: Union[str, Path, np.ndarray],
        x_col: int = 0,
        y_col: int = 1,
        key_col: int = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Assign spots to cells in a mask. The mask is a binary image where each cell is represented by a unique integer
        value. The spots are a table with the x and y coordinates of each spot. The spots are assigned to the cells by
        indexing the mask at the spot coordinates.

        :param spots: Table with the x and y coordinates of each spot.
        :param mask: Binary image where each cell is represented by a unique integer value.
        :param x_coord: Column index of the x coordinate in the spots table [default: 0].
        :param y_coord: Column index of the y coordinate in the spots table [default: 1].
        """
        self.spots = spots
        self.mask = mask
        self.labels = None
        self.assigned_spots = None
        self.background_spots = None
        self.labeled_spots = None
        self.x_col = x_col
        self.y_col = y_col
        self.key_col = key_col
        self.LOGGER = (
            logger if logger is not None else logger.set_logger(log_level="debug")
        )

        # Run the spot assignment
        self.LOGGER.debug("Assigning spots to cells...")
        self.LOGGER.debug(f"Mask dimensions: {self.mask.shape}")
        self.LOGGER.debug(f"Spots table dimensions: {self.spots.shape}")
        self.assign_spots()

    def assign_spots(self):
        """
        Assign spots to cells in a mask. The mask is a binary image where each cell is represented by a unique integer
        value. The spots are a table with the x and y coordinates of each spot. The spots are assigned to the cells by
        indexing the mask at the spot coordinates.

        Returns:
            None
        """
        # Index mask file at the spot table coordinate to get the cell id of each spot (0 for background)
        spots = self.mask[self.spots[:, self.x_col], self.spots[:, self.y_col]]
        self.LOGGER.debug(f"Total number of spots: {len(spots)}")

        # Get the unique mask labels and their counts
        # np.unique returns the sorted unique values and their frequency counts
        # The first value (index 0) is the background spot count.
        self.labels, self.assigned_spots = np.unique(spots, return_counts=True)

        # Get the number of background spots
        self.background_spots = self.assigned_spots[0]
        self.LOGGER.debug(f"Number of background spots: {self.background_spots}")

        # Get the non-zero mask labels and their counts
        self.labels = self.labels[1:]
        self.assigned_spots = self.assigned_spots[1:]
        self.LOGGER.debug(f"Number of assigned spots: {sum(self.assigned_spots)}")

        # Create an empty numpy array the size of th number of labels in the mask.
        # Fill the first column of cell_counts with the label ids
        # Assign the counts to the corresponding cell ids
        # This implementation assumes the labels are consecutive integers starting from 1
        # This needs to be adjusted accordingly if we want to preserve the original label ids
        self.labeled_spots = np.zeros((self.mask.max(), 2), dtype=np.uint32)
        self.labeled_spots[:, 0] = np.arange(1, self.mask.max() + 1)
        self.labeled_spots[self.labels - 1, 1] = self.assigned_spots

    def save(self, output_path: Union[str, Path] = None) -> None:
        """
        Save the cell assigned spots to a csv file with a header row.

        :param output_path: Path to save the cell assigned spots. If None, the function will not save the file.
        """
        np.savetxt(
            output_path,
            self.labeled_spots,
            delimiter=",",
            header="label,spot_count",
            comments="",
            fmt="%d",
        )

    def __setattr__(self, key: str, value: object) -> None:
        """
        Sets class attributes, it validates the input type for spots and mask.

        :param key: Attribute name
        :param value: Attribute value
        """
        if key == "spots":
            if isinstance(value, np.ndarray):
                self.__dict__[key] = value
            elif isinstance(value, str) or isinstance(value, Path):
                self.__dict__[key] = np.genfromtxt(
                    value, delimiter=",", skip_header=1, dtype=np.uint32
                )
            else:
                raise TypeError("Spot table must be of type np.array, string or Path.")

        elif key == "mask":
            if isinstance(value, np.ndarray):
                self.__dict__[key] = value
            elif isinstance(value, str) or isinstance(value, Path):
                self.__dict__[key] = imread(value)
            else:
                raise TypeError("Mask must be of type np.array, string or Path.")

        else:
            self.__dict__[key] = value
