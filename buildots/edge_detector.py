from time import sleep

import cv2
import os

from config import EDGE_DETECTOR_OUTPUT_DIR, IMAGE_DOWNLOADER_OUTPUT_DIR, \
    EDGE_DETECTION_INPUT, INTERVAL_TIME, THRESHOLD, PNG_THRESHOLD

PNG_EXTENSION = ".png"


class EdgeDetector:
    """
    Define edge detector object.
    """
    INPUT_DIR = os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR, EDGE_DETECTION_INPUT)

    def _get_images(self) -> None:
        """
        Get all images from downloader service.
        """
        for dir in os.listdir(EdgeDetector.INPUT_DIR):
            dir_path = os.path.join(EdgeDetector.INPUT_DIR, dir)
            for image in os.listdir(dir_path):
                threshold = THRESHOLD
                if image.endswith(PNG_EXTENSION):
                    threshold = PNG_THRESHOLD
                image_path = os.path.join(EdgeDetector.INPUT_DIR, dir, image)
                self._detect_edges(image_path, threshold)
                os.remove(image_path)

    @staticmethod
    def _detect_edges(image: str, threshold: tuple) -> None:
        """
        Detect edges of each frame, define uniq threshold if the frame source
        is png file.

        :param image: Path to image.
        :param threshold: Threshold for image type.
        """
        frame = cv2.imread(image)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, *threshold)
        image_name = os.path.basename(image)
        edges_file_name = os.path.join(EDGE_DETECTOR_OUTPUT_DIR,
                                       'edges_' + image_name)
        cv2.imwrite(edges_file_name, edges)

    def start(self) -> None:
        """
        Control the flow of the detector object.
        """
        while True:
            self._get_images()
            sleep(INTERVAL_TIME)


def main() -> None:
    """
    Initiate Detector instance and using him.
    """
    detector = EdgeDetector()
    detector.start()


if __name__ == '__main__':
    main()
