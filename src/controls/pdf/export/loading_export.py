from controls.control_container import ControlsContainer
import flet as ft
from translation import tr

class Controls(ControlsContainer):
    def __init__(self, view_container) -> None:
        super().__init__(view_container)

        self.title: ft.Text = ft.Text(
            tr("loading-preparing")
        )

        self.progress_bar: ft.ProgressBar = ft.ProgressBar(
               value=0.,
        )

        self.column: ft.Column = ft.Column(
            controls=[
                self.title,
                self.progress_bar
            ],
            # expand=True,
            # alignment=ft.MainAxisAlignment.CENTER,
        )

        self.container: ft.Container = ft.Container(
            padding=40,
            content=self.column
        )