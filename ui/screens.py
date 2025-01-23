"""Screens definition for the UI"""
from pathlib import Path
from typing import Optional

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

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
