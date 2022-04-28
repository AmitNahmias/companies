import requests
import os
import json
from time import sleep

from config import IMAGE_DOWNLOADER_INPUT_DIR, IMAGE_DOWNLOADER_OUTPUT_DIR, \
    INTERVAL_TIME, EDGE_DETECTION_INPUT, PROJECTOR_INPUT


def read_data(file_path: str) -> list:
    """
    Read data from json file contains images urls list.
    :param file_path: Path to data file.

    :return: Urls list.
    """
    f = open(file_path, 'r')
    data = json.load(f)
    return data['image_list']


class Downloader:
    """
    Define downloader object for images.
    """

    def __init__(self):
        self._urls = []

    @staticmethod
    def _download_image(url: str, image_name: str) -> None:
        """
        Download image by url path.

        :param url: Input url.
        :param image_name: Image name to save.
        """
        # Better use tenacity for example.
        try:
            response = requests.get(url)

            # Create generic folder for each image
            dir_to_save = image_name.split('.')[0]
            os.mkdir(os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR,
                                  PROJECTOR_INPUT, dir_to_save))
            os.mkdir(os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR,
                                  EDGE_DETECTION_INPUT, dir_to_save))

            first_path_to_save: str = os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR,
                                                   PROJECTOR_INPUT, dir_to_save,
                                                   image_name)
            second_path_to_save: str = os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR,
                                                    EDGE_DETECTION_INPUT,
                                                    dir_to_save,
                                                    image_name)

            file = open(first_path_to_save, 'wb')
            file.write(response.content)
            file.close()

            file = open(second_path_to_save, 'wb')
            file.write(response.content)
            file.close()

        except requests.exceptions.RequestException:
            print(f'Download failed on {url}')  # Should be in log file

    def _get_urls(self) -> None:
        """
        Gets images urls from json files according to configured input dir.
        """
        for file_name in os.listdir(IMAGE_DOWNLOADER_INPUT_DIR):
            file_path = os.path.join(IMAGE_DOWNLOADER_INPUT_DIR, file_name)
            data = read_data(file_path)
            for url in data:
                self._urls.append(url)
            os.remove(file_path)  # Deleting file to empty the input dir

    @staticmethod
    def _create_output_dirs() -> None:
        """
        Creates output dirs for other services.
        """
        for dir_name in [EDGE_DETECTION_INPUT, PROJECTOR_INPUT]:
            os.makedirs(os.path.join(IMAGE_DOWNLOADER_OUTPUT_DIR, dir_name),
                        exist_ok=True)

    def start(self) -> None:
        """
        Control the flow of the downloader object.
        """
        self._create_output_dirs()
        while True:
            self._get_urls()
            for image in self._urls:
                # The last node in the url as image name
                image_name = image.split("/")[-1]
                self._download_image(url=image, image_name=image_name)
            self._urls = []

            sleep(INTERVAL_TIME)  # Instead of watch dog


def main() -> None:
    """
    Initiate Downloader instance and using him.
    """
    downloader = Downloader()
    downloader.start()


if __name__ == '__main__':
    main()
