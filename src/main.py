import flet as ft
import os
from translation import translation_server
from views import routes
from pathlib import Path
from model.app_data import AppData


async def main(page: ft.Page) -> None:
    async def keyboard_input (event: ft.KeyboardEvent) -> None:
        match event:
            case ft.KeyboardEvent(
                key="F11"
            ):
                if page.window.full_screen:
                    page.window.full_screen = False
                else:
                    page.window.full_screen = True
                page.update()
            case _:
                await page.views[-1].container.input(event)
        
    
    async def file_picker_result(event: ft.FilePickerResultEvent) -> None:
        await page.views[-1].container.file_picker_result(event)

    page.fonts = {
        "main": "fonts/ChakraPetch-Medium.ttf"
    }
    
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.PURPLE_ACCENT,
        font_family="main",
        
    )
    # page.theme_mode =  ft.ThemeMode.LIGHT
    page.window.icon = ft.Icon(name=ft.Icons.ABC)
    

    app_data: AppData = AppData(
        assets_path=Path(os.path.dirname(os.path.abspath(__file__))) / "assets",
        prefix="isaques",
        routes=routes,
        file_picker=ft.FilePicker(
            on_result=file_picker_result
        ),
    )

    translation_server.csv_path = app_data.assets_path / "translations" / "lang.csv"
    translation_server.validade_csv()
    await translation_server.load_messages(page, app_data)

    for view_container in routes.values():
        view_container.load_app_data(page, app_data)

    page.views[0] = routes["/"].view
    page.overlay.append(app_data.file_picker)

    page.on_keyboard_event = keyboard_input


    page.title = translation_server.get_message("title")
    page.window.min_width = 900
    page.window.min_height = 720

    page.update()
    

ft.app(main)
