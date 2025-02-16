import bisect
from copy import deepcopy
from functools import partial
from pathlib import Path
from typing import Literal, Optional

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder

from utils.audio import AudioPlayer
from utils.decorators import update_time_stamp_label
from utils.enums import KeyboardEnum
from utils.kivy_extensions import message_box_info

from . import KIVY_FILE
from .manager_screen import ManagerScreen

PLS_KIVY = Path("play_audio_screen.kv")
Builder.load_file(str(KIVY_FILE / PLS_KIVY))


class PlayAudioScreen(ManagerScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_setup()
        self.audio_player: Optional[AudioPlayer] = None

    def custom_setup(self):
        """
        Custom setup for PlayAudioScreen
        """
        self.update_event = None  # Event to update the progress bar
        self.time_stamp_control = None  # Event to control the time stamp
        self._time_stamp = [0]
        self._time_stamp_index = 0

    @update_time_stamp_label
    def on_enter(self, *args):
        super().on_enter(*args)

        self.clean_events()
        self.current_audio_session = deepcopy(self.get_audio_session())
        time_stamp = self.current_audio_session.time_stamp or [0]
        self._time_stamp = time_stamp
        self._time_stamp_index = len(time_stamp) - 1  # Ostatni timestamp
        self.load_sound(self.get_audio_file())
        print(self.current_audio_session)
        # Ustawienie pozycji na ostatni time stamp
        self.audio_player.current_position = self._time_stamp[self.time_stamp_index]
        self.ids.progress_bar.value = self.audio_player.current_position
        self.ids.current_time.text = self._format_time(
            self.audio_player.current_position
        )

        Window.bind(on_key_down=self.on_key_press)

    def on_leave(self, *args):
        """When user leave the screen, unbind the key press event"""
        Window.unbind(on_key_down=self.on_key_press)
        self.current_audio_session.time_stamp = self._time_stamp
        self.update_audio_session(self.current_audio_session)
        self.custom_setup()

        super().on_leave(*args)

    def on_key_press(self, instance, key, *args):
        print("Key pressed:", key)
        key_actions = {
            KeyboardEnum.LEFT: self.reverse,
            KeyboardEnum.RIGHT: self.next,
            KeyboardEnum.UP: self.play,
            KeyboardEnum.DOWN: self.set_time_stamp,
            KeyboardEnum.SPACE: self.pause,
        }
        action = key_actions.get(key)
        if action:
            action()

    def load_sound(self, file_path: Path):
        """Ładujemy AudioPlayer objekt, następnie przypisujemy"""
        self.audio_player = AudioPlayer(file_path)

        length = self.audio_player.sound_length
        self.current_audio_session.duration = length
        self.ids.progress_bar.max = length
        self.ids.total_time.text = self._format_time(length)

    def cancel_event(self, event_name: str):
        event = getattr(self, event_name, None)
        if event:
            event.cancel()
            setattr(self, event_name, None)

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
        elif len(self._time_stamp) <= self.time_stamp_index:
            self._time_stamp_index = len(self._time_stamp) - 1

    def clean_events(self):
        """Clean the scheduled events if they exist"""
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None

        if self.time_stamp_control:
            self.time_stamp_control.cancel()
            self.time_stamp_control = None

    @update_time_stamp_label
    def set_time_stamp(self):
        """Add time stamp to the list and pause the sound"""
        current_pos = self.audio_player.get_position()
        if int(current_pos) not in [int(ts) for ts in self._time_stamp]:
            bisect.insort(self._time_stamp, current_pos)
            self.time_stamp_index += 1
        else:
            message_box_info("Time stamp already exists. You can't add it again.")
        self.pause()

    def time_stamp_range(self):
        start_idx = self.time_stamp_index
        end_idx = self.time_stamp_index + 1 if len(self._time_stamp) > 0 else None
        print("time_stamp_range", start_idx, end_idx)
        if len(self._time_stamp) <= end_idx:
            end_idx = None
        return (
            self._time_stamp[start_idx],
            self._time_stamp[end_idx] if end_idx is not None else None,
        )

    def back(self):
        if self.audio_player.sound.state == "play":
            self.audio_player.stop()

        self.manager.current = "main_screen"

    def play(self):
        """ "Audio.play() oraz ustwaienine eventów oraz zablokowanie przycisku"""
        if self.audio_player.sound.state == "stop":
            self.ids.pause_button.disabled = False
        self.audio_player.play()

        self.update_event = Clock.schedule_interval(self.update_progress_bar, 0.1)
        self.duration_time_event = Clock.schedule_interval(self.count_duration, 1)

    def count_duration(self, dt):
        if self.audio_player.sound.state == "play":
            self.current_audio_session.spend_time += 1

    def pause(self) -> None:
        """
        Pause the current sound when the user press the pause button.
        """
        if self.audio_player.sound.state == "play":
            self.ids.pause_button.disabled = True
            self.audio_player.pause()

            self.cancel_event("update_event")
            self.cancel_event("duration_time_event")

    def navigate(self, direction: Literal[1, -1]) -> None:
        """Navigate through the audio playback based on the given direction."""
        if self.audio_player.sound:
            self.time_stamp_index += direction
            if self.audio_player.sound.state == "play":
                self.audio_player.stop()

            self.audio_player.current_position = self.timer_guard()
            self.play()

    def next(self) -> None:
        """Navigate to the next time stamp in the audio playback."""
        self.navigate(1)

    def reverse(self):
        """Navigate to the previous time stamp in the audio playback."""
        self.navigate(-1)

    @update_time_stamp_label
    def timer_guard(self) -> float:
        if self.time_stamp_control:
            print("Timer guard cancelled")
            self.time_stamp_control.cancel()

        start, end = self.time_stamp_range()
        if end is not None:
            self.time_stamp_control = Clock.schedule_interval(
                partial(self.control_time, end), 0.1
            )
        return start

    def update_progress_bar(self, dt):
        if not self.audio_player:
            return

        if self.audio_player.sound:
            current_pos = self.audio_player.get_position()
            self.ids.progress_bar.value = current_pos
            self.ids.current_time.text = self._format_time(current_pos)

            if self.audio_player.is_finished():
                self.pause()
                self.current_audio_session.finished_times += 1

    @update_time_stamp_label
    def control_time(self, end, dt):
        if self.audio_player.sound:
            self.audio_player.current_position = self.audio_player.get_position()
            if self.audio_player.current_position >= end:
                if self.audio_player.sound.state == "play":
                    self.time_stamp_index += 1
                    self.pause()
                    self.timer_guard()

    @staticmethod
    def _format_time(seconds):
        """Formatuje czas w sekundach na mm:ss"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"
