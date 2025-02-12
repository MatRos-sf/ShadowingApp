from pathlib import Path
from typing import Optional

from kivy.app import App
from kivy.uix.screenmanager import Screen


class ManagerScreen(Screen):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def set_audio_file(self, audio_files: str) -> None:
        app = App.get_running_app()
        app.SELECTED_AUDIO_FILE = Path(audio_files)
        print(type(app.SELECTED_AUDIO_FILE))

    def get_audio_file(self) -> Optional[Path]:  # ? Path | str
        app = App.get_running_app()
        return app.SELECTED_AUDIO_FILE

    def create_audio():
        pass

    def update_audio():
        pass

    def list_audio():
        pass
