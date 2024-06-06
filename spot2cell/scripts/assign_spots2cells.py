import os
from pathlib import Path
import numpy as np

from tifffile import imread

print(os.name)

spots_path = Path('../../test_data/test.csv').resolve()
mask_path = Path('../../test_data/test_mask.tif').resolve()
output_path = Path('../../test_data/cell_spots.csv').resolve()

# Read spot table using numpy
spot_table = np.genfromtxt(spots_path, delimiter=',', skip_header=1, dtype=np.uint32)

# Read cell mask using tifffile
cell_mask = imread(mask_path)

# Index mask file at the spot table coordinate to get the cell id of each spot (0 for background)
spots = cell_mask[spot_table[:, 0], spot_table[:, 1]]

# Get the unique cell ids and their counts
cell_ids, counts = np.unique(spots, return_counts=True)

# Get the number of background spots
background_spots = counts[1:]

# Get the non-zero cell ids and their counts
cell_ids = cell_ids[1:]
counts = counts[1:]

# Create a zero numpy array the size of the number of cell ids in the mask
cell_spots = np.zeros((cell_mask.max(), 2), dtype=np.uint32)

# Fill the first column of cell_counts with consecutive cell ids
cell_spots[:, 0] = np.arange(1, cell_mask.max() + 1)

# Assign the counts to the corresponding cell ids
cell_spots[cell_ids-1, 1] = counts

# Save the cell spots to a csv file with a header row
np.savetxt(output_path, cell_spots, delimiter=',', header='CellID,spot_count', comments='', fmt='%d')