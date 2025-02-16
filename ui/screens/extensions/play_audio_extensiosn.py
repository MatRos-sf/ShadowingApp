__all__ = ["EventEnum", "PlayAudioEvent"]
from enum import StrEnum
from functools import partial
from typing import List, Optional

from kivy.clock import Clock

from utils.decorators import update_time_stamp_label
from utils.tools import format_time


class EventEnum(StrEnum):
    UPDATE_EVENT = "update_event"
    TIME_STAMP_CONTROL = "time_stamp_control"
    DURATION_TIME_EVENT = "duration_time_event"


class PlayAudioEvent:
    """Helper class to manage events for PlayAudioScreen instance."""

    def __init__(self):
        self.update_event = None  # Event to update the progress bar
        self.time_stamp_control = None  # Event to control the time stamp
        self.duration_time_event = None  # Event to track playback duration

    def cancel_events(self, events: Optional[List[EventEnum]] = None) -> None:
        """Cancel specified events or all events if none are specified."""
        events = events or EventEnum

        for event_name in events:
            event = getattr(self, event_name, None)
            if event:
                event.cancel()
                setattr(self, event_name, None)

    def start_play_event(
        self, tm_update_e: float = 0.1, t_duration_time_e: float = 1.0
    ) -> None:
        """Start events for updating progress bar and tracking playback duration."""
        self.update_event = Clock.schedule_interval(
            self.update_progress_bar, tm_update_e
        )
        self.duration_time_event = Clock.schedule_interval(
            self.count_duration, t_duration_time_e
        )

    def count_duration(self, dt):
        """Increase the spent time counter while audio is playing."""
        if self.audio_player.sound.state == "play":
            self.current_audio_session.spend_time += 1

    @update_time_stamp_label
    def control_time(self, end, dt):
        """Control the audio time stamp and pause if the end is reached."""
        if self.audio_player.sound:
            self.audio_player.current_position = self.audio_player.get_position()
            if self.audio_player.current_position >= end:
                if self.audio_player.sound.state == "play":
                    self.time_stamp.time_stamp_index += 1
                    self.pause()
                    self.timer_guard()

    def update_progress_bar(self, dt):
        """Update the progress bar based on the current audio position."""
        if not self.audio_player:
            return

        if self.audio_player.sound:
            current_pos = self.audio_player.get_position()
            self.ids.progress_bar.value = current_pos
            self.ids.current_time.text = format_time(current_pos)

            if self.audio_player.is_finished():
                self.pause()
                self.current_audio_session.finished_times += 1

    @update_time_stamp_label
    def timer_guard(self) -> float:
        """Ensure time stamp control is active and schedule time control event."""
        if self.time_stamp_control:
            print("Timer guard cancelled")
            self.cancel_events(["time_stamp_control"])

        start, end = self.time_stamp.range()
        if end is not None:
            self.time_stamp_control = Clock.schedule_interval(
                partial(self.control_time, end), 0.1
            )
        return start
