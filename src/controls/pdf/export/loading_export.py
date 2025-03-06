import gc
from controls.control_container import ControlsContainer
import flet as ft
from translation import tr
import os

class Controls(ControlsContainer):
    def __init__(self, view_container) -> None:
        super().__init__(view_container)

        self.title: ft.Text = ft.Text(
            tr("loading-preparing"),
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        self.progress_bar: ft.ProgressBar = ft.ProgressBar(
               value=0.,
        )

        self.continue_button: ft.FilledButton = ft.FilledButton(
            disabled=True,
            text=tr("continue"),
            on_click=self.continue_button
        )

        self.open_folder_button: ft.FilledButton = ft.FilledButton(
            text=tr("open-folder"),
            disabled=True,
            on_click= lambda x: os.startfile(self.open_folder_button.data)
        )

        self.row: ft.Row = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                self.open_folder_button,
                self.continue_button,
            ]
        )

        self.column: ft.Column = ft.Column(
            controls=[
                self.title,
                self.progress_bar,
                self.row,
            ],
            # expand=True,
            # alignment=ft.MainAxisAlignment.CENTER,
        )

        self.container: ft.Container = ft.Container(
            padding=40,
            content=self.column
        )
    
    async def continue_button(self, event) -> None:
        self.view_container.page.views[-2].container.__init__(is_reset=True)
        self.view_container.page.views[-2].container.free()
        self.view_container.page.views[-2] = self.view_container.app_data.routes["/pdffill/"].view
        await self.view_container.go_back()
        gc.collect()