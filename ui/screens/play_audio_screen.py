from copy import deepcopy
from pathlib import Path
from typing import Literal, Optional

from kivy.core.window import Window
from kivy.lang.builder import Builder

from utils.audio import AudioPlayer, TimeStampManager
from utils.decorators import update_time_stamp_label
from utils.enums import KeyboardEnum
from utils.kivy_extensions import message_box_info
from utils.tools import format_time

from . import KIVY_FILE
from .extensions import EventEnum, PlayAudioEvent
from .manager_screen import ManagerScreen

PLS_KIVY = Path("play_audio_screen.kv")
Builder.load_file(str(KIVY_FILE / PLS_KIVY))


class PlayAudioScreen(ManagerScreen, PlayAudioEvent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_player: Optional[AudioPlayer] = None
        self.time_stamp: Optional[TimeStampManager] = None

    @update_time_stamp_label
    def on_enter(self, *args):
        """Initialize the screen and load the audio file when entered."""
        self.cancel_events()
        super().on_enter(*args)

        self.current_audio_session = deepcopy(self.audio_session)
        self.load_sound(self.get_audio_file())
        Window.bind(on_key_down=self.on_key_press)

    def on_leave(self, *args):
        """Cleanup when leaving the screen, including unbinding key events."""
        Window.unbind(on_key_down=self.on_key_press)
        self.current_audio_session.time_stamp = self.time_stamp.time_stamp_list
        self.update_audio_session(self.current_audio_session)

        super().on_leave(*args)

    def on_key_press(self, instance, key, *args):
        """Handle key press events for audio control."""
        key_actions = {
            KeyboardEnum.LEFT: self.reverse,
            KeyboardEnum.RIGHT: self.next,
            KeyboardEnum.UP: self.play,
            KeyboardEnum.DOWN: self.set_time_stamp,
            KeyboardEnum.SPACE: self.pause,
            KeyboardEnum.R: self.remove_time_stamp,
        }
        print(key)
        action = key_actions.get(key)
        if action:
            action()

    def is_playing(self) -> bool:
        """Check if the audio is currently playing."""
        return self.audio_player.sound and self.audio_player.sound.state == "play"

    def load_sound(self, file_path: Path):
        """Load an audio file and initialize the player."""
        self.time_stamp = TimeStampManager(self.current_audio_session)
        self.audio_player = AudioPlayer(file_path, self.time_stamp.stamp)

        # Ustawienie pozycji na ostatni time stamp
        self.ids.progress_bar.value = self.audio_player.current_position
        self.ids.current_time.text = format_time(self.audio_player.current_position)

        # set layout after load audio
        length = self.audio_player.sound_length
        self.current_audio_session.duration = length
        self.ids.progress_bar.max = length
        self.ids.total_time.text = format_time(length)

    @update_time_stamp_label
    def set_time_stamp(self):
        """Add time stamp to the list and pause the sound"""
        current_pos = self.audio_player.get_position()
        if not self.time_stamp.add_time_stamp(current_pos):
            message_box_info("Time stamp already exists. You can't add it again.")
        self.pause()

    def back(self):
        """Stop playback and return to the main screen."""
        if self.is_playing():
            self.audio_player.stop()
        self.cancel_events()

        self.manager.current = "main_screen"

    def save(self):
        """Save the current audio session."""
        if self.is_playing():
            self.audio_player.stop()
            self.cancel_events()
        self.current_audio_session.time_stamp = self.time_stamp.time_stamp_list
        self.update_audio_session(self.current_audio_session)
        self.current_audio_session = deepcopy(self.get_audio_session())

        message_box_info("Saved!")

    def play(self):
        """Start audio playback and enable the pause button."""
        if not self.is_playing():
            self.ids.pause_button.disabled = False
        self.audio_player.play()
        self.start_play_event()

    def pause(self) -> None:
        """
        Pause the current sound when the user press the pause button.
        """
        if self.is_playing():
            self.ids.pause_button.disabled = True
            self.audio_player.pause()

            self.cancel_events([EventEnum.DURATION_TIME_EVENT, EventEnum.UPDATE_EVENT])

    def navigate(self, direction: Literal[1, -1]) -> None:
        """Navigate through the audio playback based on the given direction."""
        if self.audio_player.sound:
            self.time_stamp.time_stamp_index += direction
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
    def remove_time_stamp(self) -> None:
        """Remove the current time stamp from the audio playback."""
        try:
            self.time_stamp.remove()
        except ValueError:
            message_box_info("You can't remove the first time stamp")
        else:
            self.navigate(0)
