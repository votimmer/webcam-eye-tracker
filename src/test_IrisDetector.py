import numpy as np
import cv2 as cv
from unittest.mock import MagicMock
import pytest
from IrisDetector import IrisDetector

@pytest.fixture(scope="module")
def iris_detector():
    return IrisDetector()

def test_processImage(iris_detector):
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)

    processed_image, results = iris_detector.processImage(test_image)

    assert processed_image.shape == (480, 640, 3)
    assert isinstance(results, type(iris_detector.face_mesh.process(test_image)))

def test_detectIris_noLandmarksFound(iris_detector):
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    iris_detector.processImage = MagicMock(return_value=(test_image, MagicMock()))
    iris_detector.processImage.return_value[1].multi_face_landmarks = None
    result_image, l_cx, l_cy, r_cx, r_cy = iris_detector.detectIris(test_image)

    assert result_image.shape == test_image.shape
    assert l_cx is None
    assert l_cy is None
    assert r_cx is None
    assert r_cy is None

def test_detectIris_with_landmarks(iris_detector):
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    iris_detector.processImage = MagicMock(return_value=(test_image, MagicMock()))
    multi_face_landmarks = MagicMock()

    landmark = MagicMock()
    landmark.x = 0.5
    landmark.y = 0.5
    multi_face_landmarks.landmark = [landmark] * 478
    
    iris_detector.processImage.return_value[1].multi_face_landmarks = [multi_face_landmarks]
    result_image, l_cx, l_cy, r_cx, r_cy = iris_detector.detectIris(test_image)

    assert result_image.shape == test_image.shape
    assert isinstance(l_cx, float)
    assert isinstance(l_cy, float)
    assert isinstance(r_cx, float)
    assert isinstance(r_cy, float)