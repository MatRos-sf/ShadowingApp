from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

# from . import AUDIO_FILE_PATH

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
        app = App.get_running_app()
        # global AUDIO_FILE_PATH
        # AUDIO_FILE_PATH = self.selected_button.text
        app.SELECTED_AUDIO_FILE = self.selected_button.text
        self.manager.current = "main_screen"
