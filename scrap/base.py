from typing import List


class BaseScraper:

    def __init__(self, aligo) -> None:
        self.aligo = aligo

    def get_alishare(self, name) -> List[str]:
        ...
