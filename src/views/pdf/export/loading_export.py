from typing import override
from views.view_container import ViewContainer
from controls.pdf.export.loading_export import Controls
import flet as ft

class LoadingExport(ViewContainer):
    def __init__(self, route = None, is_reset=False) -> None:
        super().__init__(route, is_reset)

    @override
    def setup(self) -> None:
        super().setup()

        self.controls = Controls(self)

        self.view.controls.append(self.controls.container)
        self.view.vertical_alignment = ft.MainAxisAlignment.CENTER