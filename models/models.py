"""SQL models for the database."""

from sqlalchemy import DateTime, SmallInteger, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AudioModel(Base):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column()
    time_stamp: Mapped[str] = mapped_column()
    added: Mapped[DateTime] = mapped_column(default=func.now())
    duration: Mapped[int] = mapped_column(default=0)
    spend_time: Mapped[int] = mapped_column(default=0)
    finished_times: Mapped[SmallInteger] = mapped_column(default=0)
