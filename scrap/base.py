from typing import List


class BaseScraper:

    def __init__(self) -> None:
        pass

    def get_alishare(self, name) -> List[str]:
        ...
