from typing import TYPE_CHECKING
from views.view_container import ViewContainer


class ControlsContainer:
    def __init__(self, view_container: ViewContainer) -> None:
        assert isinstance(view_container, ViewContainer), "%s is not an ViewContainer!"%view_container
        self.view_container: ViewContainer = view_container