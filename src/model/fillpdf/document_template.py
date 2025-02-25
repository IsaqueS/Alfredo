from pathlib import Path
import os

class DocumentTemplate:
    def __init__(self, file_path: Path):
        assert isinstance(file_path, Path), "%s is not an Path!"%file_path
        self.file_path: Path = file_path
        if os.path.getsize(file_path) == 0:
            raise DocumentEmpty("'%s' is empty!"%file_path)
        self.text_encoding: str = "utf-8"
        self.valid_inputs: set[str] = None
        self.file = None
    
    def close_file(self) -> None:
        # print("Closed Called")
        if self.file:
            # print("Closed Executed")
            self.file.close()

    def __del__(self) -> None:
        self.close_file()

class DocumentEmpty(Exception):
    pass
