import json
import os
from collections import defaultdict
from time import sleep
from typing import List, Type

from config import INTERVAL_TIME, PROJECTOR_OUTPUT_DIR, ANALYZER_OUTPUT_DIR
from checker import Checker, Dimensions, AvgColor, BlackAndWhite

JSON_SUFFIX = '.json'


class Analyzer:
    """
    Define analyzer object.
    """

    def __init__(self):
        self._checkers: List[Type[Checker]] = [Dimensions, AvgColor,
                                               BlackAndWhite]

    @staticmethod
    def _write_output(image_path: str, data: dict) -> None:
        """
        Write data to json file.

        :param image_path: Path to image.
        :param data: Data to write.
        """
        image_name = os.path.basename(image_path).split('.')[0]
        output_json_path = os.path.join(ANALYZER_OUTPUT_DIR,
                                        image_name + JSON_SUFFIX)
        with open(output_json_path, 'w') as json_handler:
            json.dump(data, json_handler)

    def start(self) -> None:
        """
        Control the flow of the Analyzer object.
        """
        while True:
            for image in os.listdir(PROJECTOR_OUTPUT_DIR):
                json_results = defaultdict(lambda: defaultdict(dict))
                image_path = os.path.join(PROJECTOR_OUTPUT_DIR, image)
                for check in self._checkers:
                    checker_to_run = check(image_path, json_results)
                    checker_to_run.analyze()
                self._write_output(image_path=image_path, data=json_results)
                os.remove(image_path)

            sleep(INTERVAL_TIME)


def main() -> None:
    """
    Initiate Projector instance and using him.
    """
    analyzer = Analyzer()
    analyzer.start()


if __name__ == '__main__':
    main()
