from pathlib import Path

from kivy.core.audio import SoundLoader


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
