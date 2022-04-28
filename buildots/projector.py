import os
from time import sleep

import imageio as im
import numpy as np
from PIL import Image

from nfov import NFOV
from config import IMAGE_DOWNLOADER_OUTPUT_DIR, INTERVAL_TIME, PROJECTOR_INPUT, \
    PROJECTOR_OUTPUT_DIR


class Projector:
    """
    Define Projector object.
    """

    def __init__(self):
        self._nfov = NFOV()

    def _gnomonic_projection(self, image_path: str):
        """
        Perform a Gnomonic projection and save the image
        """
        img = im.imread(image_path)
        center_point = np.array([0.5, .5])
        gnomonic_projection_array = self._nfov.toNFOV(img, center_point)
        image_from_array = Image.fromarray(gnomonic_projection_array)
        image_name = os.path.basename(image_path)
        image_from_array.save(
            f'{os.path.join(PROJECTOR_OUTPUT_DIR, "processed_" + image_name)}')

    def start(self) -> None:
        """
        Control the flow of the projector object.
        """
        while True:
            for dir in os.listdir(
                    os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR, PROJECTOR_INPUT)):
                dir_path = os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR,
                                        PROJECTOR_INPUT, dir)
                for image in os.listdir(dir_path):
                    image_path = os.path.join(dir_path, image)
                    self._gnomonic_projection(image_path)
                    os.remove(image_path)
            sleep(INTERVAL_TIME)


def main() -> None:
    """
    Initiate Projector instance and using him.
    """
    projector = Projector()
    projector.start()


if __name__ == '__main__':
    main()
