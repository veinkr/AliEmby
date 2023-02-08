from aligo import Aligo
import os


class Transfer:

    def __init__(self) -> None:
        self.init_config()

        self.config = dict()

        self.dest_folder = ""

    def save_tfo(self):
        ...

    def save_ipg(self):
        ...

    def move(self, source, destnation):
        ...

    def transfer(self, source, metainfo):

        destnation = os.path.join(self.dest_folder, f"{metainfo}")

        self.move(source, destnation)
