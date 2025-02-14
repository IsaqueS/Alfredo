from views.view_container import ViewContainer
import flet as ft
from typing import override
from controls.start_view import Controls

class StartView(ViewContainer):
    
    @override
    def setup(self) -> None:
        super().setup()

        self.controls: Controls = Controls(self)

        self.view.controls.append(
            self.controls.main_column
        )

        