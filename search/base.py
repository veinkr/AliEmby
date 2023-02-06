from typing import List


class BaseSearcher:

    def __init__(self) -> None:
        pass

    def get_alishare(self, name) -> List[str]:
        ...
