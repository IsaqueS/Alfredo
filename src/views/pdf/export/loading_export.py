from typing import override
from views.view_container import ViewContainer
from controls.pdf.export.loading_export import Controls

class LoadingExport(ViewContainer):
    def __init__(self, route = None, is_reset=False) -> None:
        super().__init__(route, is_reset)

    @override
    def setup(self) -> None:
        return super().setup()

        self.controls = Controls(self)

        