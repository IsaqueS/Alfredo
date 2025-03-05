import flet as ft
from translation import tr
from controls.control_container import ControlsContainer
from typing import TYPE_CHECKING
from functools import partial

COL_SETTINGS: dict = {"sm": 6, "md": 4, "xl": 2}
COL_SETTINGS_SMALL: dict = {"sm": 6, "md": 4, "xl": 2}
COL_SETTINGS_BIG: dict = {"sm": 12, "md": 8, "xl": 4}
BUTTON_HEIGHT: int = 50

EXPORT_TYPES: dict[str,tuple[str,...]] = {
    "txt": ("txt",),
    "docx": ("docx", "pdf"),
}

if TYPE_CHECKING:
    from views.pdf.fill_pdf import FillPdf

class Controls(ControlsContainer):
    def __init__(self, view_container: "FillPdf") -> None:
        super().__init__(view_container)
        self.invalid_csv_alert: ft.AlertDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(tr("invalid-csv-title")),
            content=ft.Text("error-here",width=300,text_align=ft.TextAlign.JUSTIFY),
            actions=[
                ft.TextButton(
                    text=tr("okay"),
                    on_click=lambda x: self.view_container.page.close(self.invalid_csv_alert)
                ),
                
            ]
        )

        self.invalid_document_alert: ft.AlertDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(tr("invalid-document-title")),
            content=ft.Text("error-here",width=300,text_align=ft.TextAlign.JUSTIFY),
            actions=[
                ft.TextButton(
                    text=tr("okay"),
                    on_click=lambda x: self.view_container.page.close(self.invalid_document_alert)
                ),
                
            ]
        )

        action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)

        self.invalid_headers_banner= ft.Banner(
        bgcolor=ft.Colors.AMBER_100,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
        content=ft.Text(
            color=ft.Colors.BLACK,
        ),

       
        actions=[
            ft.TextButton(text=tr("understood"), style=action_button_style, on_click=self.close_banner),
        ],
    )

        

        self.go_back_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_ROUNDED,
            on_click=view_container.go_back
        )

        self.go_to_manual: ft.FilledButton = ft.FilledButton(
            text=tr("manual"),
            icon=ft.Icons.BOOK_ROUNDED
        )

        self.app_bar: ft.AppBar = ft.AppBar(
            leading=self.go_back_button,
            title=ft.Text(
                tr("fill-pdf-title")
            ),
            center_title=True,
            actions=[
                self.go_to_manual
            ]
            
        )

        self.open_csv_button: ft.FilledButton = ft.FilledButton(
            text=tr("open-csv"),
            icon=ft.Icons.FILE_OPEN_ROUNDED,
            col=COL_SETTINGS,
            height=BUTTON_HEIGHT
        )

        self.open_csv_button.on_click = on_click=partial(
            self.view_container.open_file,
            ["csv"],
            tr("open-csv"),
            (self.open_csv_button, "text", tr("loading-csv"))
        )

        self.open_document_button: ft.FilledButton = ft.FilledButton(
            text=tr("open-document-template"),
            icon=ft.Icons.FILE_COPY_ROUNDED,
            col=COL_SETTINGS,
            height=BUTTON_HEIGHT
        )

        self.open_document_button.on_click = on_click=partial(
            self.view_container.open_file,
            list(EXPORT_TYPES.keys()),
            tr("open-document-template"),
            (self.open_document_button, "text", tr("loading-document-template"))
        )

        self.pick_export_path_button:ft.FilledButton = ft.FilledButton(
            text=tr("open-export-path"),
            icon=ft.Icons.FOLDER_OPEN_ROUNDED,
            col=COL_SETTINGS,
            height=BUTTON_HEIGHT,
        )

        self.pick_export_path_button.on_click=partial(
            self.view_container.open_file,
            [],
            tr("open-export-path"),
            (self.pick_export_path_button, "text", tr("loading-folder")),
            is_folder = True,
        )

        self.export_file_options: ft.Dropdown = ft.Dropdown(
            width=400,
            options=[
                ft.dropdown.Option(tr("none")),
            ],
            label=tr("export-options"),
            value=tr("none"),
            col=COL_SETTINGS_SMALL,
            disabled=True,
            expand=True
        )

        self.export_button: ft.FilledButton = ft.FilledButton(
            text=tr("export"),
            icon=ft.Icons.SAVE_AS_ROUNDED,
            col=COL_SETTINGS_BIG,
            height=BUTTON_HEIGHT,
            disabled=True,
            
        )

        # col={"sm": 6, "md": 4, "xl": 2}

        self.row: ft.ResponsiveRow = ft.ResponsiveRow(
            controls=[
                self.open_csv_button,
                self.open_document_button,
                self.pick_export_path_button,
                self.export_file_options,
                self.export_button,
            ],
        )

        self.info_text: ft.Text = ft.Text(
            value=tr("csv-loading-limit-tip")
        )

        self.column: ft.Column = ft.Column(
            controls=[
                self.row,
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Text(tr("csv-import-center-msg",)),
                    expand=True
                ),
                self.info_text,
            ],
            expand=True
        )

    def show_document_error(self, msg: str) -> None:
        self.invalid_document_alert.content.value = msg
        self.view_container.page.open(self.invalid_document_alert)
        self.view_container.page.update()

    async def close_banner(self, event = None) -> None:
        if self.invalid_headers_banner.open:
            self.view_container.page.close(self.invalid_headers_banner)
    
    def open_banner(self, invalid_headers: tuple[str]) -> None:
        self.invalid_headers_banner.content.value = "%s: %s\n%s" %(
            ", ".join(
                tuple(
                    f"\"{item}\"" for item in invalid_headers
                )
            ),
            tr("not-valid-headers-warning"),
            tr("not-valid-headers-tip")
        )
        self.view_container.page.open(self.invalid_headers_banner)
    
    def reset_csv_button(self) -> None:
        if self.view_container.csv_file_title is None:
            self.open_csv_button.text = tr("open-csv")
        else:
            self.open_csv_button.text = self.view_container.csv_file_title
        self.open_csv_button.update()
    
    def reset_document_button(self) -> None:
        if self.view_container.document_template is None:
            self.open_document_button.text = tr("open-document-template")
        else:
            self.open_document_button.text = "✅ %s: %s"%(
                self.view_container.document_template.file_path.suffix.upper().replace(".",""),
                self.view_container.document_template.file_path.name,
            )
            self.update_export_options(self.view_container.document_template.file_names[-1])
        self.open_document_button.update()
    
    def update_export_options(self, file_type: str) -> None:
        export_options = EXPORT_TYPES.get(file_type,(file_type,))
        self.export_file_options.options = self.generate_export_options(export_options)
        self.export_file_options.value = export_options[0]
        self.export_file_options.disabled = False
        self.export_file_options.update()
    
    @staticmethod
    def generate_export_options(itens: tuple[str]) -> list[ft.dropdown.Option]:
        options:list[ft.dropdown.Option] = []
        for item in itens:
            options.append(
                ft.dropdown.Option(item)
            )
        return options