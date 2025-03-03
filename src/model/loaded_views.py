from typing import TYPE_CHECKING
from views import ViewContainer

if TYPE_CHECKING:
    from views import ViewContainer
    import flet as ft

class LoadedViews:
    def __init__(self, page: "ft.Page", max_size: int = 5) -> None:
        self.__loaded_views: list["ViewContainer"] = []
        self.__MAX_SIZE: int = max_size
        self.__PAGE:"ft.Page" = page
    
    async def add(self, view_container: "ViewContainer") -> None:
        assert isinstance(view_container, ViewContainer), "%s is not an ViewContainer!"%view_container
        self.__loaded_views.append(view_container)
        loaded_views: int = len(self.__loaded_views)

        if loaded_views > self.__MAX_SIZE:
            
            current_index: int = 0

            for i in range(loaded_views - 1):
                deleted_view: ViewContainer = self.__loaded_views[current_index]
                if deleted_view.view in self.__PAGE.views:
                    current_index += 1
                    continue

                deleted_view.__init__(is_reset=True)
                deleted_view.free()
                self.__loaded_views.pop(0)

                if len(self.__loaded_views) <= self.__MAX_SIZE:
                    break
    
    def remove_view(self, view: "ft.View") -> None:
        for view_container in self.__loaded_views:
            if view_container.view == view:
                view_container.__init__(is_reset=True)
                view_container.free()
                self.__loaded_views.remove(view_container)