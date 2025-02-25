from views.view_container import ViewContainer
import flet as ft
from typing import override
from controls.start_view import Controls
import asyncio

class StartView(ViewContainer):
    
    @override
    def setup(self) -> None:
        super().setup()

        self.controls: Controls = Controls(self)

        self.view.controls.append(
            self.controls.main_column
        )
        self.page.run_task(self.animate_image)

    async def animate_image(self) -> None:
        await asyncio.sleep(.5)

        self.controls.title_image.opacity = 1.
        self.controls.title_image.offset = ft.Offset(0,0)
        self.controls.title_text.opacity = 1.
        self.controls.title_text.offset = ft.Offset(0,0)
        self.controls.title_image.update()
        self.controls.title_text.update()

        