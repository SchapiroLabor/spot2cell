import os
from pathlib import Path

class Spot2Cell:
    def __init__(self, path):
        self.path = Path(path)
        self.spot2cell_path = self.path / 'spot2cell'
        self.spot2cell_script = self.spot2cell_path / 'spot2cell.py'
        self.spot2cell_script = self.spot2cell_script.resolve()
        self.spot2cell_script = str(self.spot2cell_script)

