import pytest

from main import ShadowApp


class TestApp:
    def setup_method(self):
        self.app = ShadowApp()
        self.gui = self.app.build()

    def test_gui_exists(self):
        assert self.gui is not None

    def test_app_should_have_4_screens(self):
        assert len(self.gui.screens) == 4

    def test_current_screen_should_be_main_screen(self):
        assert self.gui.current == "main_screen"

    @pytest.mark.parametrize(
        "screen_name",
        ["main_screen", "file_chooser_screen", "read_file_screen", "play_audio_screen"],
    )
    def test_app_should_have_screen(self, screen_name):
        assert screen_name in [s.name for s in self.gui.screens]
