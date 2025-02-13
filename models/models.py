"""SQL models for the database."""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .db_setup import Base


class AudioModel(Base):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column(unique=True)
    time_stamp: Mapped[str] = mapped_column(
        comment="This field represents the timestamp, separated by a comma"
    )
    added: Mapped[datetime] = mapped_column(server_default=func.now())
    duration: Mapped[int] = mapped_column(
        default=0, comment="Duration of the audio in seconds"
    )
    spend_time: Mapped[int] = mapped_column(
        default=0, comment="Total time the audio was played, in seconds"
    )
    finished_times: Mapped[int] = mapped_column(
        default=0, comment="Number of times the audio was finished"
    )
