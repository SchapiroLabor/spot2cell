import os
from pathlib import Path
import numpy as np
from tifffile import imread

print(os.name)

# read in csv file using numpy
data = np.genfromtxt('data.csv', delimiter=',', skip_header=1)
