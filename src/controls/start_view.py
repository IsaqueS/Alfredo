import math
import flet as ft
from controls.control_container import ControlsContainer
from translation import tr
from functools import partial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.main.start_view import StartView

BUTTON_WIDTH: int = 320


class Controls(ControlsContainer):
    def __init__(self, view_container: "StartView"):
        super().__init__(view_container)

        self.settings_button: ft.ElevatedButton = ft.ElevatedButton(
            icon= ft.Icons.SETTINGS_ROUNDED,
            text = tr("settings"),
        )
        self.manual_button:ft.ElevatedButton = ft.ElevatedButton(
            text=tr("manual"),
            icon=ft.Icons.MENU_BOOK_ROUNDED,
        )

        self.title_image: ft.Image = ft.Image(
            src=f"icon.png",
            fit=ft.ImageFit.FIT_WIDTH,
            animate_opacity=500,
            animate_offset=ft.Animation(
                500,
                ft.AnimationCurve.EASE_OUT_CUBIC,
            ),
            opacity=0.,
            offset=ft.Offset(0,.2),
        )

        self.title_text: ft.Text = ft.Text(
            value=tr("start-title"),
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            text_align=ft.TextAlign.CENTER,
            animate_opacity=500,
            animate_offset=ft.Animation(
                500,
                ft.AnimationCurve.EASE_OUT_CUBIC,
            ),
            opacity=0.,
            offset=ft.Offset(0,.2),
        )
    

        self.image_container: ft.Container = ft.Container(
            alignment= ft.alignment.center,
            content=self.title_image,
            height=200,
            bgcolor=ft.Colors.RED_100,
            border_radius=20,
             gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[
                    "0xff9c1904",
                    "0xffdd0956",
                ],
            ),
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
            width=BUTTON_WIDTH
        )
        
        self.button_column: ft.Column = ft.Column(
            controls=[
                self.fill_pdf_button,
                ft.FilledButton(tr("coming-soon"),width=BUTTON_WIDTH,disabled=True),
            ],
        )

        self.main_column: ft.Column = ft.Column(
            controls=[
                self.image_stack,
                ft.Row(
                    controls=[
                        self.title_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            self.button_column
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                ),
                ft.Text("%s: %s - IsaqueS"%(
                    tr("version"),
                    self.view_container.app_data.version,
                ))
            ],
            expand=True,
        )

        