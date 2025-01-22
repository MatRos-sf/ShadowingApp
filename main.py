"""Application starting point"""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from ui.screens import FileChooser

Window.size = (900, 800)


class ShadowApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FileChooser(name="file_chooser_screen"))
        sm.current = "file_chooser_screen"
        return sm


if __name__ == "__main__":
    ShadowApp().run()
