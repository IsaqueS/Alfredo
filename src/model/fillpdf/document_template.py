from pathlib import Path
import os
from typing import Optional, Callable

class DocumentTemplate:
    def __init__(self, file_path: Path):
        assert isinstance(file_path, Path), "%s is not an Path!"%file_path
        self.file_path: Path = file_path
        self.file = None
        if os.path.getsize(file_path) == 0:
            raise DocumentEmpty("'%s' is empty!"%file_path)
        self.text_encoding: str = "utf-8"
        self.valid_inputs: set[str] = set()
        self.file_names: tuple[str] = tuple(self.file_path.name.split("."))
        self.amount_done: float = 0.
        self.total_to_be_done: float = None
        self.paths_used: dict = {}
        self._current_export_function: Callable = self.export
        self.export_type: str = self.file_names[-1]
    
    def close_file(self) -> None:
        # print("Closed Called")
        if self.file:
            # print("Closed Executed")
            self.file.close()
    
    @property
    def current_export_function(self) -> Callable:
        return self._current_export_function
    
    def set_export_type(self, file_type: str) -> None:
        assert isinstance(file_type, str), "%s is not an string!"%file_type
        self.export_type = file_type
    
    def export(self, headers: tuple[str, ...], data: tuple[str, ...], path: Path) -> Optional[tuple[str,...]]:
        assert isinstance(path, Path), "%s is not an Path object!"%path
        assert isinstance(headers, tuple), "%s is not an tuple!"
        assert isinstance(data, tuple), "%s is not an tuple!"
    
    def get_file_path(self,data:tuple[str,...]) -> str:
        name: str = "%s - %s.%s"%(
            self.file_names[0],
            " - ".join(data),
            self.file_names[-1],
        )

        get_index: int | None = self.paths_used.get(name, None)

        if isinstance(get_index, int):
            self.paths_used[name] = get_index + 1
            name = "%s - %s(%s).%s"%(
                self.file_names[0],
                " - ".join(data),
                get_index,
                self.file_names[-1],
            )
        else:
            self.paths_used[name] = 1

        return name

    def set_counter(self, amount: float) -> None:
        self.amount_done = 0.
        self.total_to_be_done = float(amount)
    
    def add_to_counter(self) -> None:
        self.amount_done += 1
    
    def get_progress(self) -> float:
        return self.amount_done / self.total_to_be_done

    def prepare_export(self) -> None: # Executes before export
        pass
    
    def clean_export(self) -> None: # Executes after export
        pass

    def __del__(self) -> None:
        self.close_file()

class DocumentEmpty(Exception):
    pass

class DocumentWithNoInputs(Exception):
    pass
