from pathlib import Path
import flet as ft
from views.view_container import ViewContainer
from typing import override
from translation import tr
from model.fillpdf.csv import CSV, InvalidCSVHeader
from model.fillpdf.document_template import DocumentTemplate, DocumentEmpty
from model.fillpdf.document_templates import TXTTemplate
import asyncio
import os
from controls.pdf.fill_pdf import Controls


class FillPdf(ViewContainer):
    def __init__(self, route: str = None, is_reset = False):
        super().__init__(route, is_reset)

        self.csv_encoding: str = "utf-8"
        self.csv: CSV = None
        self.document_path: Path = None
        self.csv_file_title: str = None
        self.document_template: DocumentTemplate = None
        self.button_file_types: set = set()
        self.export_folder: Path = None
        
    @override
    def setup(self) -> None:
        super().setup()

        self.controls = Controls(self)

        self.view.controls.append(self.controls.app_bar)
        self.view.controls.append(self.controls.column)

    @override
    async def input(self, event: ft.KeyboardEvent) -> None:
        match event:
            case ft.KeyboardEvent(
                key = "Escape"
            ):
                await self.go_back()
    
    @override
    async def file_picker_result(self, event: ft.FilePickerResultEvent) -> None:

        is_folder = False
        file_path:Path = None

        if event.files is None:
            self.controls.reset_csv_button()
            self.controls.reset_document_button()
            if event.path:
                is_folder = True
                file_path = Path(event.path)
            else:
                if isinstance(self.export_folder, Path):
                    self.controls.pick_export_path_button.text = "✅ %s"%self.export_folder.name
                    self.controls.pick_export_path_button.update()
                else:
                    self.controls.pick_export_path_button.text = tr("open-export-path")
                    self.controls.pick_export_path_button.update()
                return
        else:
            file_path = Path(event.files[0].path)

        if is_folder:
            self.export_folder = file_path
            self.controls.pick_export_path_button.text = "✅ %s"%file_path.name
            self.controls.pick_export_path_button.update()
            self.page.run_task(
                self.export_button_enabler
            )

        if file_path.suffix == "":
            self.controls.reset_csv_button()
            self.controls.reset_document_button()
            return

        match file_path.suffix.lower():
            case ".csv":
                await self.validate_csv(file_path)
            case ".txt":
                try:
                    self.document_template = TXTTemplate(file_path)
                except DocumentEmpty as e:
                    self.controls.invalid_document_alert.content.value = tr("empty-document-error")
                    self.page.open(
                        self.controls.invalid_document_alert
                    )
                    self.page.update()
                self.controls.reset_document_button()
                


        self.page.run_task(self.export_button_enabler)

        if self.on_current_view():
            self.view.update()
    
    async def open_file(self, extensions: list[str],
        title: str, change_attr: tuple[object, str, object], event: ft.ControlEvent=None,is_folder: bool = False) -> None:

        if isinstance(change_attr,tuple):
            setattr(change_attr[0],change_attr[1],change_attr[2])
            self.view.update()

        if is_folder:
            await asyncio.sleep(0.05) # HACK: For some reason 'get_directory_path' freezes the app on windows...
            self.app_data.file_picker.get_directory_path(
                dialog_title=title,
            )
        else:
            self.app_data.file_picker.pick_files(
                    dialog_title=title,
                    allow_multiple=False,
                    file_type=ft.FilePickerFileType.CUSTOM,
                    allowed_extensions=extensions
                )

            self.button_file_types = set(extensions)

        

    def get_table(self, csv:CSV) -> ft.DataTable:

        data_columns: list[ft.DataColumn] = []

        for column in csv.data.keys():
            is_numeric: bool = False

            first_value: str = csv.data[column][0]

            try:
                float(first_value)
                is_numeric = True
            except ValueError:
                pass
            
            tool_tip: str = None

            # if is_numeric: # Disabled because theres an bug with the text
            #     tool_tip: str = tr("is-numeric-tooltip")
            # else:
            #     tool_tip: str = tr("not-numeric-tooltip")

            data_columns.append(
                ft.DataColumn(
                    ft.Text(column),
                    numeric=is_numeric,
                    tooltip=tool_tip, 
                )
            )
        
        data_rows: list[ft.DataRow] = []

        try:
            for index in range(500): # Limited for performance reasons...
                cells: list[ft.DataCell] = []
                
                for column in csv.data.keys():
                    cells.append(
                        ft.DataCell(
                            content=ft.Text(
                                value=csv.data[column][index]
                            )
                        )
                    )
                
                data_rows.append(
                    ft.DataRow(
                        cells=cells
                    )
                )
        except KeyError:
            pass
        except IndexError:
            pass
            
        return ft.DataTable(
            columns=data_columns,
            rows=data_rows,
            expand=True,
            vertical_lines=ft.BorderSide(3, ft.Colors.BLUE_700),
            horizontal_lines=ft.BorderSide(1, ft.Colors.BLUE_400),
            opacity=0,
            animate_opacity=320
        )

    async def load_csv(self, file_path: Path) -> None:
        new_csv: CSV = CSV(file_path,self.csv_encoding)
        
        await asyncio.sleep(0)

        await new_csv.read_csv()
        self.csv = new_csv
        self.controls.info_text.value = "%s: %s, %s: %s, %s: %s, %s: %s"%(
            tr("valid-headers"),
            ", ".join(self.csv.valid_headers),
            tr("columns"),
            len(self.csv.valid_headers),
            tr("rows"),
            len(self.csv.data[self.csv.valid_headers[0]]),
            tr("invalid-headers"),
            ", ".join(self.csv.invalid_headers) if len(self.csv.invalid_headers) > 0 else tr("none"),
        )

        if len(self.csv.invalid_headers) > 0:
            self.controls.open_banner(self.csv.invalid_headers)
        else:
            await self.controls.close_banner()
        
        await asyncio.sleep(0)

        table: ft.DataTable = self.get_table(self.csv)

        self.controls.column.controls[1] = ft.ListView(
            controls=[table],
            expand=True,
        )

        self.csv_file_title = "✅ CSV: %s"%file_path.name
        self.controls.open_csv_button.text = self.csv_file_title

        await asyncio.sleep(0)

        if self.on_current_view(): 
            self.view.update()
        
        await asyncio.sleep(.2)
        table.opacity = 1.

    async def validate_csv(self, file_path: Path) -> None:
        if not os.path.getsize(file_path) == 0:    
            try:
                self.controls.open_csv_button.text = tr("processing-csv")
                self.controls.open_csv_button.update()

                load_csv_task: asyncio.Task[None] = asyncio.create_task(self.load_csv(file_path))

                await load_csv_task
                
            except InvalidCSVHeader:
                self.controls.invalid_csv_alert.content.value = "%s\n\n%s"%(
                    tr("invalid-header"),
                    tr("valid-header-example")
                )
                self.page.open(self.controls.invalid_csv_alert)
                self.controls.reset_csv_button()
            except Exception as e:
                self.controls.invalid_csv_alert.content.value = "%s\n\n%s: %s"%(
                    tr("csv-generic-error"),
                    tr("error"),
                    e,
                )
                self.page.open(self.controls.invalid_csv_alert)
                self.controls.reset_csv_button()
        else:
            self.controls.invalid_csv_alert.content.value = tr("empty-csv-error")
            self.page.open(self.controls.invalid_csv_alert)
            self.controls.reset_csv_button()

    def validade_export(self) -> bool:
        return True if self.csv and self.document_template and self.export_folder else False

    async def export_button_enabler(self):
        self.controls.export_button.disabled = not self.validade_export()
        self.controls.export_button.update()