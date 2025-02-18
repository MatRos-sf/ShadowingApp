from pathlib import Path

from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from . import KIVY_FILE
from .manager_screen import ManagerScreen

RFS_KIVY = Path("read_file_screen.kv")

Builder.load_file(str(KIVY_FILE / RFS_KIVY))


class ReadFileScreen(ManagerScreen):
    selected_button = None

    def on_enter(self, *args):
        """
        When the screen is entered, create dynamic buttons with recently selected files
        """
        # Remove any existing widget in the ScrollView
        self.list_of_audio_session = self.list_audio()
        self.ids.scroll_view.clear_widgets()

        # create dynamic buttons
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))
        for row in self.list_of_audio_session:
            btn = Button(text=str(row.file_path), size_hint_y=None, height=40)
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
        selected_file = Path(self.selected_button.text)
        self.audio_session = next(
            (
                session
                for session in self.list_of_audio_session
                if session.file_path == selected_file
            ),
            None,
        )
        self.manager.current = "main_screen"
