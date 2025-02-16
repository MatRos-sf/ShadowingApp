import bisect
from pathlib import Path

from kivy.core.audio import SoundLoader

from models.session_manager import AudioSession


class AudioLoadError(Exception):
    """Custom exceptions for audio loading failures"""


class AudioPlayer:
    def __init__(self, audio_path: Path, current_position=0):
        self.sound = SoundLoader.load(str(audio_path))
        if not self.sound:
            raise ValueError("Could not load sound!")  # TODO: Maybe custom exceptions
        self.sound_length = self.sound.length or 0
        self.current_position = current_position

    def play(self):
        self.sound.seek(self.current_position)
        self.sound.play()

    def stop(self):
        self.sound.stop()

    def pause(self):
        """Pause the current sound and set new current_position value"""
        self.current_position = self.get_position()
        self.stop()

    def get_position(self):
        return self.sound.get_pos()

    def is_finished(self) -> bool:
        return self.get_position() >= self.sound_length

    def cleanup(self):
        """Explicitly unload resources"""
        if self.sound:
            self.sound.unload()


class TimeStampManager:
    def __init__(self, audio_session: AudioSession):
        self._time_stamp_list = audio_session.time_stamp or [0]
        self._time_stamp_index = len(self._time_stamp_list) - 1

    @property
    def stamp(self):
        return self._time_stamp_list[self._time_stamp_index]

    @property
    def time_stamp_list(self):
        return self._time_stamp_list

    # time stamp section
    @property
    def time_stamp_index(self):
        return self._time_stamp_index

    @time_stamp_index.setter
    def time_stamp_index(self, value):
        """
        Set the time stam index for audio playback

        If the value is less than 0, it is set to 0. If the value exceeds the
        number of available time stamps, it is set to the last valid index.
        """
        self._time_stamp_index = value

        if self.time_stamp_index < 0:
            self._time_stamp_index = 0
        elif len(self._time_stamp_list) <= self.time_stamp_index:
            self._time_stamp_index = len(self._time_stamp_list) - 1

    def add_time_stamp(self, new_position) -> bool:
        if int(new_position) not in [int(ts) for ts in self._time_stamp_list]:
            bisect.insort(self._time_stamp_list, new_position)
            self.time_stamp_index += 1
            return True
        return False

    def range(self):
        if len(self._time_stamp_list) == 1:
            return 0, None

        start = self._time_stamp_list[self.time_stamp_index]
        end = (
            self._time_stamp_list[self.time_stamp_index + 1]
            if self.time_stamp_index + 1 < len(self._time_stamp_list)
            else None
        )
        return start, end
