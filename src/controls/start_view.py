import flet as ft
from controls.control_container import ControlsContainer
from translation import tr
from functools import partial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.main.start_view import StartView


class Controls(ControlsContainer):
    def __init__(self, view_container: "StartView"):
        super().__init__(view_container)

        self.settings_button: ft.OutlinedButton = ft.OutlinedButton(
            icon= ft.Icons.SETTINGS_ROUNDED,
            text = tr("settings"),
        )
        self.manual_button:ft.OutlinedButton = ft.OutlinedButton(
            text=tr("manual"),
            icon=ft.Icons.MENU_BOOK_ROUNDED,
        )

        self.title_image: ft.Image = ft.Image(
            src=f"icon.png",
            fit=ft.ImageFit.FIT_WIDTH,
            
        )

        self.image_container: ft.Container = ft.Container(
            alignment= ft.alignment.center,
            content=self.title_image,
            height=200,
            bgcolor=ft.Colors.RED_100,
            border_radius=20,
        )

        self.image_stack: ft.Stack = ft.Stack(
            controls=[
                self.image_container,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            self.settings_button,
                            self.manual_button,
                       ],
                        tight=True,
                    
                    ),
                margin=8
                )
                
            ],
            alignment=ft.alignment.bottom_left
        )

        self.fill_pdf_button: ft.FilledButton = ft.FilledButton(
            text=tr("fill-pdfs-button"),
            icon=ft.Icons.EDIT_DOCUMENT,
            on_click=partial(view_container.go_to_next_view,"/pdffill/"),
        )
        

        self.main_column: ft.Column = ft.Column(
            controls=[
                self.image_stack,
                self.fill_pdf_button,
            ],
            alignment=ft.alignment.center

        )