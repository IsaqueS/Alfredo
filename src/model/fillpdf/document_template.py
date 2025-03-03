from pathlib import Path
import os
from typing import Optional

class DocumentTemplate:
    def __init__(self, file_path: Path):
        assert isinstance(file_path, Path), "%s is not an Path!"%file_path
        self.file_path: Path = file_path
        if os.path.getsize(file_path) == 0:
            raise DocumentEmpty("'%s' is empty!"%file_path)
        self.text_encoding: str = "utf-8"
        self.valid_inputs: set[str] = None
        self.file = None
        self.file_names: tuple[str] = tuple(self.file_path.name.split("."))
        self.amount_done: float = 0.
        self.total_to_be_done: float = None
        self.paths_used: set = set()
    
    def close_file(self) -> None:
        # print("Closed Called")
        if self.file:
            # print("Closed Executed")
            self.file.close()
    
    def export(self, headers: tuple[str, ...], data: tuple[str, ...], path: Path) -> Optional[tuple[str,...]]:
        assert isinstance(path, Path), "%s is not an Path object!"%path
    
    def get_file_path(self,data:tuple[str,...]) -> str:
        name: str = "%s - %s.%s"%(
            self.file_names[0],
            " - ".join(data),
            self.file_names[-1],
        )
        if name in self.paths_used:
            file_index: int = 1
            name = "%s - %s(%s).%s"%(
                self.file_names[0],
                " - ".join(data),
                file_index,
                self.file_names[-1],
            )
            while name in self.paths_used:
                file_index += 1
                name = "%s - %s(%s).%s"%(
                    self.file_names[0],
                    " - ".join(data),
                    file_index,
                    self.file_names[-1],
                )

        self.paths_used.add(name)
        return name

    def set_counter(self, amount: float) -> None:
        self.amount_done = 0.
        self.total_to_be_done = float(amount)
    
    def add_to_counter(self) -> None:
        self.amount_done += 1
    
    def get_progress(self) -> float:
        return self.amount_done / self.total_to_be_done    

    def __del__(self) -> None:
        self.close_file()

class DocumentEmpty(Exception):
    pass
