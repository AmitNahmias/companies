from datetime import datetime


class Licence:
    def __init__(self, start: datetime, end: datetime):
        self._start = start
        self._end = end

    def get_start(self) -> datetime:
        return self._start

    def get_end(self) -> datetime:
        return self._end


def sort(a: set) -> set:
    pass


def get_space(licences: set):
    licences = sort(licences)
    end = licences[0].get_end()
    for licence in licences[:-1]:
        if licence.get_end() > end:
            end = licence.get_end()
        elif end < licences[-1].get_start():
            return end
        else:
            return licences[-1].get_end()

# |-------------1|
#                   |2-------------|
#                                 |3-------|
