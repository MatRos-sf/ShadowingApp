"""SQL models for the database."""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .db_setup import Base


class AudioModel(Base):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()
    time_stamp: Mapped[str] = mapped_column()
    added: Mapped[datetime] = mapped_column(server_default=func.now())
    duration: Mapped[int] = mapped_column(default=0)
    spend_time: Mapped[int] = mapped_column(default=0)
    finished_times: Mapped[int] = mapped_column(default=0)
