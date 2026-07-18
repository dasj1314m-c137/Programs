import flet as ft

MOBILE_BREAKPOINT = 750

class ResponsiveLayout:
    def __init__(self, page: ft.Page):
        self.page = page
        self._is_mobile = (page.window.width or 1200) < MOBILE_BREAKPOINT
        self._rebuild_callback = None

    @property
    def is_mobile(self) -> bool:
        return self._is_mobile

    def set_rebuild_callback(self, callback):
        self._rebuild_callback = callback

    def on_resize(self, e):
        new_width = e.width
        if new_width is None:
            return
        was_mobile = self._is_mobile
        self._is_mobile = new_width < MOBILE_BREAKPOINT
        if was_mobile != self._is_mobile and self._rebuild_callback:
            self._rebuild_callback()

    def get_content_padding(self) -> int:
        return 10 if self._is_mobile else 20

    def get_title_size(self) -> int:
        return 16 if self._is_mobile else 20

    def get_button_height(self) -> int:
        return 45 if self._is_mobile else 50

    def get_button_width(self) -> int | None:
        return None if self._is_mobile else 250

    def get_input_max_lines(self) -> int:
        return 4 if self._is_mobile else 7

    def get_option_list_height(self, count: int) -> int | None:
        if count > 5:
            return 150 if self._is_mobile else 180
        return None
