from pathlib import Path

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from . import KIVY_FILE

M_KIVY = Path("main_screen.kv")

Builder.load_file(str(KIVY_FILE / M_KIVY))


class MainScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        if not app.SELECTED_AUDIO_FILE:
            self.ids.play_button.disabled = True
        else:
            self.ids.play_button.disabled = False
            self.ids.info_label.text = (
                f"Selected audio: {Path(app.SELECTED_AUDIO_FILE).name}"
            )

    def read_file(self):
        self.manager.current = "read_file_screen"

    def choose_file(self):
        self.manager.current = "file_chooser_screen"

    def play(self):
        self.manager.current = "play_audio_screen"
