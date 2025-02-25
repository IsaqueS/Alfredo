import flet as ft
import asyncio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.app_data import AppData

class ViewContainer():
    def __init__(self, route: str = None, is_reset = False) -> None:
        if not is_reset:
            self.__VIEW: ft.View = None
            self.__ROUTE: str = route
            self.page: ft.Page = None
            self.__APP_DATA:  "AppData" = None
    
    async def input(self, event: ft.KeyboardEvent) -> None:
        pass

    async def file_picker_result(self, event:ft.FilePickerResultEvent) -> None:
        pass
    
    def load_app_data(self, page: ft.Page, app_data: "AppData") -> None:
        self.page = page
        self.__APP_DATA = app_data

    def setup(self)-> None:
        self.__VIEW = ft.View(route=self.__ROUTE)
        self.view.container = self
    
    @property
    def route(self) -> str:
        assert self.__VIEW is None, "Please initiate View First!"
        return self.__VIEW.route

    @property
    def view(self) -> ft.View:
        if self.__VIEW is None:
            self.setup()
            self.page.run_task(self.app_data.loaded_views.add, self)
        return self.__VIEW
    
    @property
    def routes(self) -> dict[str,"ViewContainer"]:
        return self.__APP_DATA.routes

    @property
    def app_data(self) -> "AppData":
        return self.__APP_DATA
    
    async def go_back(self, event: ft.ControlEvent = None) -> None:
        self.page.views.pop()
        self.page.update()
    
    async def go_to_next_view(self, route: str,event: ft.ControlEvent) -> None:
        self.page.views.append(self.routes[route].view)
        self.page.update()
    
    def free(self) -> None:
        self.__VIEW = None
        if hasattr(self, "controls"):
            self.controls = None
        print("%s was freed!"% self)

    def on_current_view(self) -> bool:
        return self.page.views[-1] == self.__VIEW
    


        