from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from views import ViewContainer
    import flet as ft
    from pathlib import Path


VERSION: str = "0.1.0"

@dataclass
class AppData:
    assets_path: "Path"
    prefix: str
    routes: dict[str,"ViewContainer"]
    file_picker: "ft.FilePicker"
    version: str = VERSION