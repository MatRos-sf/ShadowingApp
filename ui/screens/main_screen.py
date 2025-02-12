from pathlib import Path

from kivy.lang.builder import Builder

from . import KIVY_FILE
from .manager_screen import ManagerScreen

M_KIVY = Path("main_screen.kv")

Builder.load_file(str(KIVY_FILE / M_KIVY))


class MainScreen(ManagerScreen):
    def on_enter(self, *args):
        audio_file = self.get_audio_file()
        if not audio_file:
            self.ids.play_button.disabled = True
        else:
            self.ids.play_button.disabled = False
            self.ids.info_label.text = f"Selected audio: {audio_file.name}"

    def read_file(self):
        self.manager.current = "read_file_screen"

    def choose_file(self):
        self.manager.current = "file_chooser_screen"

    def play(self):
        self.manager.current = "play_audio_screen"
