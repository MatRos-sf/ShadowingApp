from dataclasses import dataclass
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
    file_path: str
    time_stamp: List[float]
    duration: int
    spend_time: int
    finished_times: int

    @classmethod
    def parse_data(cls, data: tuple) -> "AudioSession":
        data["time_stamp"] = [float(i) for i in data["time_stamp"]]
        print(data)
        return AudioSession(**data)
