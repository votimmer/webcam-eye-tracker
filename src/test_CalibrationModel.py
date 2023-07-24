from CalibrationModel import CalibrationModel
import pytest 
import os
from datetime import datetime
import csv
import math

@pytest.fixture
def square_model():
    return CalibrationModel(3,3,1500, 1920, 1080, 'c')

@pytest.fixture
def rectangular_model():
    return CalibrationModel(3,5,1000, 1920, 1080, 'c')

def test_setSamples(square_model):
    test = 30
    square_model.setSamples(test)
    assert square_model.samples == test

def test_divideScreenSizeSquare(square_model):
    size = len(square_model.divideScreen())
    assert size == 9

def test_divideScreenSizeRect(rectangular_model):
    size = len(rectangular_model.divideScreen())
    assert size == 15

def test_divideScreenSquare(square_model):
    square_model.setWindowDimensions(300, 300)
    cells = square_model.divideScreen().sort()
    control = [(50, 50), (150, 50), (250, 50), (50, 150), (150, 150), (250, 150), (50, 250), (150, 250), (250, 250)].sort()
    assert cells == control

def test_divideScreenRect():
    smallcm = CalibrationModel(1, 3, 1000, 300, 300, 'c')
    cells = smallcm.divideScreen().sort()
    control = [(50, 150), (150, 50), (250, 50)].sort()
    assert cells == control

def test_divideScreen_zero(capsys):
    zerocm = CalibrationModel(0, 3, 1000, 300, 300, 'c')
    assert zerocm.unvisited is None

def test_unvisitedCells(square_model):
    cells = square_model.divideScreen()
    assert square_model.unvisited.sort() == cells.sort()

def test_visitCellRemoved(square_model): 
    """Tests whether cell is removed from list of unvisited cells after being visited by visual marker."""
    square_model.setWindowDimensions(300, 300)
    cell = (50, 150)
    square_model.visitCell(cell)
    assert square_model.unvisited.count(cell) == 0

def test_visitCellVisited():
    """Tests whether a cell that has been visited is added to the list containing all visited cells."""
    square_model2 = CalibrationModel(3,3,1500, 300, 300, 'c')
    cell = (50, 150)
    square_model2.visitCell(cell)
    assert square_model2.visited.count(cell) == 1
    assert len(square_model2.visited) == 1

def test_checkAllVisitedTrue(square_model):
    """Tests whether function returns True if all cells have been visited."""
    size = len(square_model.unvisited)
    for i in range(size):
        cell = square_model.unvisited[0]
        square_model.visitCell(cell)
    assert square_model.checkAllVisited() == True

def test_checkAllVisitedFalse(rectangular_model):
    """Checks whether function returns False if not all cells have been visited."""
    cell = rectangular_model.unvisited[0]
    rectangular_model.visitCell(cell)
    assert rectangular_model.checkAllVisited() == False

def test_checkAllVisited_none(rectangular_model, capsys):
    rectangular_model.unvisited = None
    rectangular_model.checkAllVisited()
    captured = capsys.readouterr()
    assert captured.out == "The list containing unvisited cells does not exist.\n"

def test_createFile(square_model):
    square_model.createFile()
    assert square_model.output_file is not None
    assert os.path.isfile(square_model.output_file)

def test_createFile_headers(square_model): 
    """Checks whether the output file contains the correct headers."""
    square_model.createFile()

    with open(square_model.output_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        assert header == ['Dot location x', 'Dot location y', 
                             'Left eye x-coordinates', 'Left eye y-coordinates', 
                             'Right eye x-coordinates', 'Right eye y-coordinates',
                             'Iris Distance']

def test_writeToFile(square_model):
    """Checks whether new data is written to the file in the correct manner."""
    square_model.createFile()
    square_model.writeToFile((10, 20), (30, 40), (50, 60), 70)

    with open(square_model.output_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  #Skip header
        row = next(reader)
        assert row == ["10", "20", "30", "40", "50", "60", "70"]

def test_createFileNewFile(square_model):
    """Checks whether a new file is created,"""
    square_model.createFile()
    assert os.path.exists('data_{}.csv'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))

def test_createFileHeaders(square_model):
    """Checks whether the headers are written to the file."""
    square_model.createFile()
    with open(square_model.output_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        assert headers == ['Dot location x', 'Dot location y', 
                             'Left eye x-coordinates', 'Left eye y-coordinates', 
                             'Right eye x-coordinates', 'Right eye y-coordinates',
                             'Iris Distance']

def test_calculateDistance(square_model):
    test = square_model.calculateDistance((5,6), (3,4))
    assert test == math.sqrt(8)

def test_calculateAverageDistance(square_model):
    test = [2,4,6]
    result = square_model.calculateAverageDistance(test)
    assert result == 4

def test_calculateAverageDistance_empty_list(square_model):
    test = []
    result = square_model.calculateAverageDistance(test)
    assert result is None

def test_collectSamples_exception(square_model, capsys):
    square_model.collectSamples(0, (2,5))
    captured = capsys.readouterr()
    assert captured.out == "Samples must be larger than 0\n"

    



