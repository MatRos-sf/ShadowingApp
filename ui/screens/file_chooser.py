from pathlib import Path

from kivy.lang.builder import Builder

from . import KIVY_FILE
from .manager_screen import ManagerScreen

FCH_KIVY = Path("file_chooser.kv")

Builder.load_file(str(KIVY_FILE / FCH_KIVY))


class FileChooser(ManagerScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the initial path for FileChooserIconView to the Home directory
        self.ids.file_chooser.path = str(Path.home())

    def selected(self, file_name):
        try:
            self.ids.selected_label.text = f"Selected audio: {file_name[0]}"
        except IndexError:
            pass

    def choose(self):
        """Sets the selected audio file and moves to the main screen"""
        self.set_audio_file(self.ids.file_chooser.selection[0])
        self.get_or_create_audio(self.get_audio_file())
        self.manager.current = "main_screen"

    def cancel(self):
        self.manager.current = "main_screen"
