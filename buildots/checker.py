from abc import abstractmethod, ABC
from PIL import Image
import numpy as np
import cv2


class Checker(ABC):
    def __init__(self, image_path: str, results: dict):
        """

        :param image_path:
        :param results:
        """
        self._image_path = image_path
        self._results = results

    @abstractmethod
    def analyze(self) -> None:
        """
        Analyze single image and append the result to the json file.
        """
        pass


class Dimensions(Checker):
    """
    Define dimensions checker.
    """

    def analyze(self):
        img = Image.open(self._image_path)
        width, height = img.size
        self._results['dimensions']['height'] = height
        self._results['dimensions']['width'] = width


class AvgColor(Checker):
    """
    Define AvgColor checker.
    """

    def analyze(self):
        src_img = cv2.imread(self._image_path)
        average_color_row = np.average(src_img, axis=0)
        average_color = np.average(average_color_row, axis=0)
        red, green, blue = average_color
        self._results['avg_color']['red'] = red
        self._results['avg_color']['green'] = green
        self._results['avg_color']['blue'] = blue


class BlackAndWhite(Checker):
    """
    Define black and white checker.
    """
    def analyze(self):
        src_img = cv2.imread(self._image_path)
        black_and_white_image = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        average_color_row = np.average(black_and_white_image, axis=0)
        average_color = np.average(average_color_row, axis=0)
        gray = average_color
        self._results['avg_black_and_white']['gray'] = gray
        # self._results['avg_black_and_white']['white'] = white
