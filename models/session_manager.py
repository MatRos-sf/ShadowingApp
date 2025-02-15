from dataclasses import dataclass
from pathlib import Path
from typing import List

from .db_setup import SessionLocal


class DataBaseSessionManager:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, traceback):
        if self.session:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
            self.session.close()


@dataclass
class AudioSession:
    id: int
    name: str
    file_path: Path
    time_stamp: List[float]
    duration: int
    spend_time: int
    finished_times: int

    @classmethod
    def parse_data(cls, data: tuple) -> "AudioSession":
        time_stamp = [float(i) for i in data.pop("time_stamp")]
        file_path = Path(data.pop("file_path"))
        return cls(**data, time_stamp=time_stamp, file_path=file_path)
