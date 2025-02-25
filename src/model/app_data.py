from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from views import ViewContainer
    import flet as ft
    from model.loaded_views import LoadedViews

VERSION: str = "0.1.0"

@dataclass
class AppData:
    assets_path: Path
    prefix: str
    routes: dict[str,"ViewContainer"]
    file_picker: "ft.FilePicker"
    loaded_views: "LoadedViews"
    version: str = VERSION