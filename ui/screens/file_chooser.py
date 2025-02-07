from pathlib import Path

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from . import KIVY_FILE

FCH_KIVY = Path("file_chooser.kv")

Builder.load_file(str(KIVY_FILE / FCH_KIVY))


class FileChooser(Screen):
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
        app = App.get_running_app()
        app.SELECTED_AUDIO_FILE = self.ids.file_chooser.selection[0]
        self.manager.current = "main_screen"

    def cancel(self):
        self.manager.current = "main_screen"
