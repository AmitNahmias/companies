import hashlib
import os
from collections import defaultdict


class Scanner:
    def __init__(self, path: str):
        self._path = path
        self._db = defaultdict(list)

    def _hash_all_files(self) -> None:
        for r, d, f in os.walk(self._path):
            for file in f:
                # if file.endswith('.txt'):
                    file_path = os.path.join(r, file)
                    try:
                        with open(file_path) as file_handler:
                            data = file_handler.read()
                            hash_result = hashlib.md5(data.encode())
                            self._db[hash_result.hexdigest()].append(file_path)
                    except Exception:
                        print()

    def print_results(self) -> None:
        self._hash_all_files()
        for item in self._db:
            if len(self._db[item]) > 1:
                print(self._db[item])


# s = Scanner(path='D:\PyCharm\PycharmProjects\companies\zoomin')
# s.print_results()

with open('D:\\PyCharm\\PycharmProjects\\companies\\zoomin\\venv\\Lib\\site-packages\\pip\\_vendor\\pyparsing.py') as file_handler:
    data = file_handler.read()
    hash_result = hashlib.md5(data.encode())
    print(hash_result)
