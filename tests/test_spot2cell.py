import pytest
import numpy as np
from tempfile import NamedTemporaryFile
from tifffile import imwrite
import os
from spot2cell import Spot2Cell

# Pytest.fixture is a decorator that allows you to define a factory for test objects.
@pytest.fixture
def setup_spot2cell():
    # Create a sample spots array
    spots = np.array([
        [1, 4],
        [2, 2],
        [3, 3],
        [4, 4],
        [5, 5]
    ])

    # Create a sample mask array
    mask = np.array([
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 2, 2, 0],
        [0, 0, 0, 2, 2, 0],
        [0, 0, 0, 0, 0, 0]
    ])

    # Temporary file for saving results
    temp_file = NamedTemporaryFile(delete=False, suffix='.csv')
    temp_file_path = temp_file.name
    temp_file.close()

    yield spots, mask, temp_file_path

    # Clean up
    os.remove(temp_file_path)


def test_spot2cell_initialization(setup_spot2cell):
    """
    This test checks if the Spot2Cell class is initialized correctly.
    :param setup_spot2cell: A fixture that returns a sample spots array, mask array, and a temporary file path.
    :return:
    """
    spots, mask, _ = setup_spot2cell
    s2c = Spot2Cell(spots, mask)
    np.testing.assert_array_equal(s2c.spots, spots)
    np.testing.assert_array_equal(s2c.mask, mask)


def test_spot2cell_counts(setup_spot2cell):
    """
    This test checks if the Spot2Cell class correctly assigns spots to cells.
    In this case the expected counts are: 2 spots assigned to cell 1, 2 spots assigned to cell 2.
    :param setup_spot2cell:
    :return:
    """
    spots, mask, _ = setup_spot2cell
    s2c = Spot2Cell(spots, mask)
    expected_counts = np.array([[1, 1], [2, 2]], dtype=np.uint32)
    np.testing.assert_array_equal(s2c.cell_spots, expected_counts)


def test_spot2cell_save(setup_spot2cell):
    """
    This test checks if the Spot2Cell class correctly saves the assigned spots to a csv file.
    The expected counts are: 2 spots assigned to cell 1, 2 spots assigned to cell 2.
    :param setup_spot2cell:
    :return:
    """
    spots, mask, temp_file_path = setup_spot2cell
    s2c = Spot2Cell(spots, mask)
    s2c.save(temp_file_path)

    # Read back the saved file
    loaded_data = np.genfromtxt(temp_file_path, delimiter=',', skip_header=1, dtype=np.uint32)
    expected_counts = np.array([[1, 1], [2, 2]], dtype=np.uint32)
    np.testing.assert_array_equal(loaded_data, expected_counts)


def test_spot2cell_mask_from_file(setup_spot2cell):
    """
    This test checks if the Spot2Cell class correctly reads the mask from a tif file.
    :param setup_spot2cell:
    :return:
    """
    spots, mask, _ = setup_spot2cell
    with NamedTemporaryFile(delete=False, suffix='.tif') as temp_mask_file:
        imwrite(temp_mask_file.name, mask)
        temp_mask_file_path = temp_mask_file.name
        s2c = Spot2Cell(spots, temp_mask_file_path)
        np.testing.assert_array_equal(s2c.mask, mask)


def test_spot2cell_spots_from_file(setup_spot2cell):
    """
    This test checks if the Spot2Cell class correctly reads spots from a csv file.
    :param setup_spot2cell:
    :return:
    """
    spots, mask, _ = setup_spot2cell
    with NamedTemporaryFile(delete=False, suffix='.csv') as temp_spots_file:
        np.savetxt(temp_spots_file.name, spots, delimiter=',', header='y,x', comments='', fmt='%d')
        temp_spots_file_path = temp_spots_file.name
        s2c = Spot2Cell(temp_spots_file_path, mask)
        np.testing.assert_array_equal(s2c.spots, spots)
