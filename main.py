"""Application starting point"""
from pathlib import Path
from typing import Optional

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from models.db_setup import Base, engine
from models.models import AudioModel  # noqa: F401
from models.session_manager import AudioSession
from ui.screens.file_chooser import FileChooser
from ui.screens.main_screen import MainScreen
from ui.screens.play_audio_screen import PlayAudioScreen
from ui.screens.read_file_screen import ReadFileScreen

Window.size = (900, 800)


class ShadowApp(App):
    SELECTED_AUDIO_FILE: Optional[Path] = None
    AUDIO_SESSION: Optional[AudioSession] = None

    def build(self) -> ScreenManager:
        Base.metadata.create_all(bind=engine)

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(FileChooser(name="file_chooser_screen"))
        sm.add_widget(PlayAudioScreen(name="play_audio_screen"))
        sm.add_widget(ReadFileScreen(name="read_file_screen"))
        sm.current = "main_screen"
        return sm


if __name__ == "__main__":
    ShadowApp().run()
