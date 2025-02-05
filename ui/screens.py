"""Screens definition for the UI"""
import bisect
from functools import partial
from pathlib import Path
from typing import Literal, Optional

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from utils.decorators import update_time_stamp_label
from utils.enums import KeyboardEnum
from utils.kivy_extensions import message_box_info

SAMPLE_FILES_PATH = [
    "/home/user/documents",
    "/var/log/system.log",
    "/etc/nginx/nginx.conf",
    "/usr/local/bin/script.sh",
    "/opt/software/config.yaml",
    "/mnt/storage/backups",
    "/dev/sda1",
    "/proc/cpuinfo",
    "/sys/kernel/debug",
]
KIVY_FILE = Path(__file__).parent / Path("kv") / Path("main_screen.kv")
Builder.load_file(str(KIVY_FILE))

AUDIO_FILE_PATH: Optional[str] = None


class MainScreen(Screen):
    def on_enter(self, *args):
        if not AUDIO_FILE_PATH:
            self.ids.play_button.disabled = True
        else:
            self.ids.play_button.disabled = False
            self.ids.info_label.text = f"Selected audio: {Path(AUDIO_FILE_PATH).name}"

    def read_file(self):
        self.manager.current = "read_file_screen"

    def choose_file(self):
        self.manager.current = "file_chooser_screen"

    def play(self):
        self.manager.current = "play_audio_screen"


class FileChooser(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the initial path for FileChooserIconView to the Home directory
        self.ids.file_chooser.path = str(Path.home())

    def selected(self, file_name):
        try:
            self.ids.selected_label.text = f"Selected audio: {file_name[0]}"
        except IndexError:
            pass

    def choose(self):
        """Sets the selected audio file and moves to the main screen"""
        global AUDIO_FILE_PATH
        AUDIO_FILE_PATH = self.ids.file_chooser.selection[0]
        self.manager.current = "main_screen"

    def cancel(self):
        self.manager.current = "main_screen"


class ReadFileScreen(Screen):
    selected_button = None

    def on_enter(self, *args):
        """
        When the screen is entered, create dynamic buttons with recently selected files
        """
        # Remove any existing widget in the ScrollView
        self.ids.scroll_view.clear_widgets()

        # create dynamic buttons
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        for path in SAMPLE_FILES_PATH:
            btn = Button(text=path, size_hint_y=None, height=40)
            btn.bind(on_press=self.on_button_click)
            layout.add_widget(btn)
        self.ids.scroll_view.add_widget(layout)

    def on_button_click(self, instance):
        # Reset color of previously selected button
        if self.selected_button or instance == self.selected_button:
            self.selected_button.background_color = [1, 1, 1, 1]  # Default white color
            if instance == self.selected_button:
                self.selected_button = None
                self.ids.button_choose.disabled = False
                self.ids.chose_file.text = ""
                return

        # Update selected button, change its color and enable the "Choose" button
        self.selected_button = instance
        self.ids.button_choose.disabled = False
        self.ids.chose_file.text = f"Selected file: {instance.text}"
        self.selected_button.background_color = [0, 0.5, 1, 1]

    def back(self):
        """
        Back to the menu and reset:
            * selected_button attribute
            * chose_file text
        """
        self.manager.current = "main_screen"
        self.selected_button = None
        self.ids.chose_file.text = ""

    def choose(self):
        global AUDIO_FILE_PATH
        AUDIO_FILE_PATH = self.selected_button.text
        self.manager.current = "main_screen"


class PlayAudioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_setup()
        Window.bind(on_key_down=self.on_key_press)

    def custom_setup(self):
        """
        Custom setup for PlayAudioScreen
        """
        self.sound: Optional[SoundLoader] = None
        self.update_event = None  # Event to update the progress bar
        self.time_stamp_control = None  # Event to control the time stamp
        self.current_position = 0
        self._time_stamp = [0]
        self._time_stamp_index = 0

    def on_enter(self, *args):
        super().on_enter(*args)
        self.sound = SoundLoader.load(str(AUDIO_FILE_PATH))
        if self.sound:
            self.ids.progress_bar.max = self.sound.length
            self.ids.total_time.text = self._format_time(self.sound.length)
        else:
            print("Failed to load sound")

    def on_leave(self, *args):
        """When user leave the screen, unbind the key press event"""
        global AUDIO_FILE_PATH
        AUDIO_FILE_PATH = None
        self.custom_setup()

        Window.unbind(on_key_down=self.on_key_press)
        return super().on_leave(*args)

    def on_key_press(self, instance, key, *args):
        print("Key pressed:", key)

        match key:
            case KeyboardEnum.LEFT:
                self.reverse()
            case KeyboardEnum.RIGHT:
                self.next()
            case KeyboardEnum.UP:
                self.play()
            case KeyboardEnum.DOWN:
                self.set_time_stamp()
            case KeyboardEnum.SPACE:
                self.pause()

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

    @update_time_stamp_label
    def set_time_stamp(self):
        """Add time stamp to the list and pause the sound"""
        current_pos = self.sound.get_pos()
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
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None

        self.manager.current = "main_screen"

    def play(self):
        if self.sound:
            if self.sound.state == "stop":
                self.ids.pause_button.disabled = False
                self.sound.seek(self.current_position)
            self.sound.play()
            self.update_event = Clock.schedule_interval(self.update_progress_bar, 0.1)

    def pause(self) -> None:
        """
        Pause the current sound when the user press the pause button.

        The following actions are performed:
            - Stops the sound playback if it is currently playing.
            - Cancels the scheduled update event
            - Saves the current position of the sound for resuming later.
            - Disables the pause button to prevent further interaction.
        """
        if self.sound:
            if self.sound.state == "play":
                self.ids.pause_button.disabled = True
                self.current_position = self.sound.get_pos()
                self.sound.stop()
                if self.update_event:
                    self.update_event.cancel()
                    self.update_event = None

    def navigate(self, direction: Literal[1, -1]) -> None:
        """Navigate through the audio playback based on the given direction."""
        if self.sound:
            self.time_stamp_index += direction
            if self.sound.state == "play":
                self.sound.stop()

            start = self.timer_guard()
            self.seek(start)
            self.play()

    def next(self) -> None:
        """Navigate to the next time stamp in the audio playback."""
        self.navigate(1)

    def reverse(self):
        """Navigate to the previous time stamp in the audio playback."""
        self.navigate(-1)

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
        if self.sound:
            current_pos = self.sound.get_pos()
            self.ids.progress_bar.value = current_pos
            self.ids.current_time.text = self._format_time(current_pos)

            if current_pos >= self.sound.length:
                self.pause()

    @update_time_stamp_label
    def control_time(self, end, dt):
        current_pos = self.sound.get_pos()
        if current_pos >= end:
            if self.sound.state == "play":
                self.time_stamp_index += 1
                self.pause()
                self.timer_guard()

    def seek(self, position):
        """Seek do określonej pozycji w dźwięku"""
        if self.sound:
            self.sound.seek(position)

    @staticmethod
    def _format_time(seconds):
        """Formatuje czas w sekundach na mm:ss"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"
