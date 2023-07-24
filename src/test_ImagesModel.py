from ImagesModel import ImagesModel
import pytest
import os
import csv

@pytest.fixture
def images_model():
    return ImagesModel(1500)

def test_populate_image_list_length(images_model, tmp_path):
    """Checks whether the length of the list is correct after adding valid files."""
    d = tmp_path / "sub"
    d.mkdir()
    (d / "test1.jpg").write_text("random")
    (d / "test2.png").write_text("random")
    (d / "file.txt").write_text("random")

    images_model.populate_image_list(str(d))

    assert len(images_model.images) == 2

def test_populate_image_list_length_validcontent(images_model, tmp_path):
    """Ensures that files with valid extensions are added to the image list."""
    d = tmp_path / "sub"
    d.mkdir()
    (d / "test1.jpg").write_text("random")
    (d / "test2.png").write_text("random")
    (d / "file.txt").write_text("random")

    images_model.populate_image_list(str(d))

    assert str(d / "test1.jpg") in images_model.images
    assert str(d / "test2.png") in images_model.images

def test_populate_image_list_length_invalidcontent(images_model, tmp_path):
    """Ensures that files with invalid extensions aren't added to the image list."""
    d = tmp_path / "sub"
    d.mkdir()
    (d / "test1.jpg").write_text("random")
    (d / "test2.png").write_text("random")
    (d / "file.txt").write_text("random")

    images_model.populate_image_list(str(d))

    assert str(d / "file.txt") not in images_model.images

def test_populate_image_list_empty(images_model):
    """Tests whether an invalid file path returns an empty list."""
    images_model.populate_image_list("invalid/file/path")
    assert len(images_model.images) == 0

def test_createFile(images_model):
    """Checks whether an output file is created."""
    images_model.createFile()
    assert images_model.output_file is not None
    assert os.path.isfile(images_model.output_file)

def test_createFile_headers(images_model):
    """Checks whether the output file contains the correct headers."""
    images_model.createFile()

    with open(images_model.output_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        assert header == ['Image', 'Gaze location x', 'Gaze location y']

def test_writeToFile(images_model):
    """Checks whether new data is written to the file in the correct manner."""
    images_model.createFile()
    images_model.writeToFile("test.jpg", 10, 20)

    with open(images_model.output_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  #Skip header
        row = next(reader)
        assert row == ["test.jpg", "10", "20"]



