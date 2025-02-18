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
    def parse_data(cls, data: dict) -> "AudioSession":
        data = data.copy()
        time_stamp = data.pop("time_stamp", None)
        time_stamp = [float(i) for i in time_stamp.split(",")] if time_stamp else []
        file_path = Path(data.pop("file_path"))
        return cls(**data, time_stamp=time_stamp, file_path=file_path)

    def to_dict(self) -> dict:
        audio_session = self.__dict__.copy()
        # convert list to str
        audio_session["time_stamp"] = ",".join(map(str, audio_session["time_stamp"]))
        audio_session["file_path"] = str(audio_session["file_path"])
        return audio_session

    def diff(self, other: "AudioSession") -> dict:
        if not isinstance(other, AudioSession):
            raise ValueError("Can only compare with another AudioSession instance.")
        difference = {}
        other = other.to_dict()
        self_dict = self.to_dict()
        for key in self_dict.keys():
            if self_dict[key] != other[key]:
                difference[key] = other[key]

        return difference
