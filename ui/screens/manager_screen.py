from pathlib import Path
from typing import Optional

from kivy.app import App
from kivy.uix.screenmanager import Screen

from models.models import AudioModel
from models.session_manager import DataBaseSessionManager
from utils.kivy_extensions import message_box_info


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

    def create_audio(self, file_path: Path, *args):
        with DataBaseSessionManager() as session:
            audio = AudioModel(
                name=str(file_path.name), file_path=str(file_path), time_stamp=""
            )
            session.add(audio)
            session.commit()

    def update_audio():
        pass

    def list_audio():
        pass

    def find_audio(self, audio_name: str):
        with DataBaseSessionManager() as session:
            audio = session.query(AudioModel).filter_by(name=audio_name).first()
            return audio

    def get_or_create_audio(self, audio_path: Path):
        audio = self.find_audio(audio_path.name)

        if audio is None:
            audio = self.create_audio(audio_path)
        else:
            message_box_info(
                "Audio already exists in the database and stats will be imported."
            )
        return audio
