import flet as ft

MOBILE_BREAKPOINT = 750

class ResponsiveLayout:
    def __init__(self, page: ft.Page, platform=None):
        self.page = page
        self._is_mobile = (page.window.width or 1200) < MOBILE_BREAKPOINT
        self._rebuild_callback = None
        self._is_mobile_platform = platform in (
            ft.PagePlatform.ANDROID, ft.PagePlatform.IOS
        ) if platform else False
        self.responsive_mobile = self._is_mobile or self._is_mobile_platform

    @property
    def is_mobile(self) -> bool:
        return self.responsive_mobile

    def set_rebuild_callback(self, callback):
        self._rebuild_callback = callback

    def on_resize(self, e):
        new_width = e.width
        if new_width is None:
            return
        was_mobile = self._is_mobile
        self._is_mobile = new_width < MOBILE_BREAKPOINT
        if was_mobile != self._is_mobile and self._rebuild_callback:
            self.responsive_mobile = self._is_mobile or self._is_mobile_platform
            self._rebuild_callback()

    def get_content_padding(self) -> int:
        return 2 if self.responsive_mobile else 10

    def get_title_size(self) -> int:
        return 16 if self.responsive_mobile else 20

    def get_button_height(self) -> int:
        return 45 if self.responsive_mobile else 50

    def get_button_width(self) -> int | None:
        return None if self.responsive_mobile else 250

    def get_input_max_lines(self) -> int:
        return 4 if self.responsive_mobile else 7

    def get_option_list_height(self, count: int) -> int | None:
        if not self.responsive_mobile and count > 5:
            return 180
        elif self.responsive_mobile and count > 3:
            return 130
        return None

    def get_spacing(self):
        return -3 if self.responsive_mobile else 6

    def get_margin(self):
        return 0 if self.responsive_mobile else 10
