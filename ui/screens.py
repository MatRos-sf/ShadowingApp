"""Screens definition for the UI"""
from pathlib import Path
from typing import Optional

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

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
        self.sound: Optional[SoundLoader] = None
        self.update_event = None  # Event dla aktualizacji slidera
        self.current_position = 0

    def on_enter(self, *args):
        super().on_enter(*args)
        self.sound = SoundLoader.load(str(AUDIO_FILE_PATH))
        if self.sound:
            print(f"Sound found at {self.sound.source}")
            print(f"Sound is {self.sound.length:.3f} seconds")
            self.ids.progress_bar.max = self.sound.length
            self.ids.total_time.text = self._format_time(self.sound.length)
        else:
            print("Failed to load sound")

    def back(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None

        self.manager.current = "main_screen"

    def play(self):
        if self.sound:
            if self.sound.state == "stop":
                self.sound.seek(self.current_position)
            self.sound.play()
            self.update_event = Clock.schedule_interval(self.update_progress_bar, 0.1)

    def pause(self):
        if self.sound:
            if self.sound.state == "play":
                self.current_position = self.sound.get_pos()
                self.sound.stop()
                if self.update_event:
                    self.update_event.cancel()
                    self.update_event = None

    def update_progress_bar(self, dt):
        if self.sound:
            current_pos = self.sound.get_pos()
            self.ids.progress_bar.value = current_pos
            self.ids.current_time.text = self._format_time(current_pos)

            if current_pos >= self.sound.length:
                self.pause()

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
