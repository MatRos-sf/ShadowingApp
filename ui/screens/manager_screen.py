from pathlib import Path
from typing import List, Optional

from kivy.app import App
from kivy.uix.screenmanager import Screen
from sqlalchemy import select

from models.models import AudioModel
from models.session_manager import AudioSession, DataBaseSessionManager
from utils.kivy_extensions import message_box_info


class ManagerScreen(Screen):
    # these fields are neccessary to create AudioSession
    FIELD_TO_SESSION = (
        AudioModel.id,
        AudioModel.name,
        AudioModel.file_path,
        AudioModel.time_stamp,
        AudioModel.spend_time,
        AudioModel.finished_times,
        AudioModel.duration,
    )

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def set_audio_file(self, audio_files: str) -> None:
        app = App.get_running_app()
        app.SELECTED_AUDIO_FILE = Path(audio_files)
        print(type(app.SELECTED_AUDIO_FILE))

    def get_audio_file(self) -> Optional[Path]:  # ? Path | str
        app = App.get_running_app()
        return app.SELECTED_AUDIO_FILE

    def set_audio_session(self, audio_session: AudioSession):
        app = App.get_running_app()
        app.AUDIO_SESSION = audio_session

    def get_audio_session(self) -> Optional[AudioSession]:
        app = App.get_running_app()
        return app.AUDIO_SESSION

    # TODO: compare audio session

    def create_audio(self, file_path: Path, *args) -> AudioSession:
        audio = AudioModel(
            name=str(file_path.name), file_path=str(file_path), time_stamp=""
        )
        with DataBaseSessionManager() as session:
            audio = AudioModel(
                name=str(file_path.name), file_path=str(file_path), time_stamp=""
            )
            session.add(audio)
            session.commit()
            return AudioSession(
                id=audio.id,
                name=audio.name,
                file_path=audio.file_path,
                time_stamp=[],
                spend_time=audio.spend_time,
                finished_times=audio.finished_times,
                duration=audio.duration,
            )

    def update_audio():
        pass

    def list_audio(self) -> List[AudioSession]:
        stmt = select(*self.FIELD_TO_SESSION).order_by(AudioModel.added)

        results = []
        with DataBaseSessionManager() as session:
            for row in session.execute(stmt).all():
                results.append(AudioSession.parse_data(row._asdict()))

        return results

    def find_audio(self, audio_name: str) -> Optional[AudioSession]:
        stmt = select(*self.FIELD_TO_SESSION).where(AudioModel.name == audio_name)

        with DataBaseSessionManager() as session:
            audio = session.execute(stmt).first()
            return AudioSession.parse_data(audio._asdict()) if audio else None

    def get_or_create_audio(self, audio_path: Path) -> AudioSession:
        audio = self.find_audio(audio_path.name)
        if audio is None:
            audio = self.create_audio(audio_path)
        else:
            message_box_info(
                "Audio already exists in the database and stats will be imported."
            )
        return audio
