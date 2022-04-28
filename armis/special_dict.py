from datetime import datetime


class SpecialDict(dict):
    def __init__(self):
        super().__init__()
        self._all_value = None
        self._set_all_time = None

    def set(self, key, value) -> None:
        self[key] = [value, datetime.now()]

    def get(self, key):
        if self._set_all_time is None or self[key][1] > self._set_all_time:
            return self[key][0]
        else:
            return self._all_value

    def set_all(self, value):
        self._all_value = value
        self._set_all_time = datetime.now()


sd = SpecialDict()
sd.set(1, 'a')
sd.set(2, 'b')
print(sd.get(1))  # expected  to a
sd.set_all('c')
print(sd.get(1))  # expected  to c
