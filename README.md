# spot2cell
[![PyPI](https://img.shields.io/pypi/v/spot2cell?style=flat-square)](https://pypi.org/project/spot2cell/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spot2cell?style=flat-square)](https://pypi.org/project/spot2cell/)
[![PyPI - License](https://img.shields.io/pypi/l/spot2cell?style=flat-square)](https://pypi.org/project/spot2cell/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/spot2cell)](https://pypistats.org/packages/spot2cell)
[![main](https://github.com/saezlab/liana-py/actions/workflows/main.yml/badge.svg)](https://github.com/schapirolabor/spot2cell/actions)

Spot2cell is a tool that assigns spots to labeled masks with minimum instalation requirements.  
It aims to provide a simple, easy-to-use way for assigning spots to cell masks.

## Installation
spot2cell is available on PyPI and Conda-Forge and can be installed using `pip` or `conda`.

Install using `pip`:
```bash
pip install spot2cell
```

Install using `conda`:
```bash
conda install -c conda-forge spot2cell
```

## Docker

Build Docker image from Dockerfile
```bash
docker build -t spot2cell .
```

## CLI

```bash
spot2cell --help

usage: spots2cells.py [-h] [-s SPOTS] [-m MASK] [-x X_COL] [-y Y_COL] [-o OUTPUT] [--verbose] [--version]

This scripts assigns a list of spots to the objects in an instance mask.

options:
  -h, --help           show this help message and exit
  -s, --spots SPOTS    Path to the spot table file.
  -m, --mask MASK      Path to the isntance mask file.
  -x, --x-col X_COL    Column index of the x coordinate in the spots table [default: 0].
  -y, --y-col Y_COL    Column index of the y coordinate in the spots table [default: 1].
  -o, --output OUTPUT  Path to the output csv file.
  --verbose            Verbose logging.
  --version            show programs version number and exit
```
## Expected Inputs
Spot2cell expects two inputs:
- `spots`: A comma-separated `.csv` table of spots with x and y coordinates. 
- `mask`: An instance mask `.tif` file. In which each object is labeled with a unique positive number and each pixel belongs to exactly one object.
