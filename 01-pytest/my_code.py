import csv
import requests
from typing import Optional


class FirstClass:
    def __init__(self):
        self.var = None
        self.data = None

    def double_pos_int(self, pos_value: int) -> int:
        if pos_value <= 0:
            raise RuntimeError("Pos value should be greater 0.")
        return pos_value * 2

    def add_two_numbers(self, a: int, b: int) -> int:
        return a + b

    def unpack_dict(self, input_dict: dict) -> list[int]:
        return [val for val in input_dict.values()]


class SecondClass:
    def __init__(self, url):
        self.url = url

    def add_to_remote_number(self, num: int, key: str) -> Optional[int]:
        """Gets the number which corresponds to `key` from the endpoint and adds num to it."""
        res = self._get_request(self.url)
        remote_number = res.get(key)
        return remote_number + num if remote_number else None

    def _get_request(self, url: str) -> dict[str, int]:
        """Example return data: {'ten': 10, 'three': 3}"""
        res = requests.get(url=url, params={"key": "value"})
        res.raise_for_status()
        return res.json()


class ThirdClass:
    def __init__(self):
        pass

    def write_to_csv(self, filename: str, data: list[list[str]]) -> None:
        """Writes data to a csv file."""
        with open(filename, "w", encoding="utf-8") as filehandler:
            writer = csv.writer(filehandler)
            for row in data:
                writer.writerow(row)


if __name__ == "__main__":
    c = ThirdClass()
    data = [["A", 2], ["B", 3]]
    c.write_to_csv("testfile.csv", data)
