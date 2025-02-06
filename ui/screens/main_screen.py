from pathlib import Path

from kivy.app import App
from kivy.uix.screenmanager import Screen

# from . import AUDIO_FILE_PATH


class MainScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        # if not AUDIO_FILE_PATH:
        if not app.SELECTED_AUDIO_FILE:
            self.ids.play_button.disabled = True
        else:
            self.ids.play_button.disabled = False
            # self.ids.info_label.text = f"Selected audio: {Path(AUDIO_FILE_PATH).name}"
            self.ids.info_label.text = (
                f"Selected audio: {Path(app.SELECTED_AUDIO_FILE).name}"
            )

    def read_file(self):
        self.manager.current = "read_file_screen"

    def choose_file(self):
        self.manager.current = "file_chooser_screen"

    def play(self):
        self.manager.current = "play_audio_screen"
