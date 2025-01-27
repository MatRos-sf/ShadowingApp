"""Application starting point"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from ui.screens import FileChooser, MainScreen, PlayAudioScreen, ReadFileScreen

Window.size = (900, 800)


class ShadowApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(FileChooser(name="file_chooser_screen"))
        sm.add_widget(PlayAudioScreen(name="play_audio_screen"))
        sm.add_widget(ReadFileScreen(name="read_file_screen"))
        sm.current = "main_screen"
        return sm


if __name__ == "__main__":
    ShadowApp().run()
