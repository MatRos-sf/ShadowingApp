import unittest
from unittest.mock import patch

from kivy.uix.button import Button
from kivy.uix.label import Label

# Import your MainScreen class
from ui.screens import MainScreen


class TestMainScreen(unittest.TestCase):
    def setUp(self):
        # Create the MainScreen instance
        self.main_screen = MainScreen(name="main_screen")

    def test_widgets_exist(self):
        # Check if all buttons and labels exist
        self.assertIsNotNone(
            self.main_screen.ids.choose_file_button, "Choose File Button does not exist"
        )
        self.assertIsNotNone(
            self.main_screen.ids.read_file_button, "Read File Button does not exist"
        )
        self.assertIsNotNone(
            self.main_screen.ids.play_button, "Play Button does not exist"
        )
        self.assertIsNotNone(
            self.main_screen.ids.info_label, "Info Label does not exist"
        )

    def test_play_button_not_disabled(self):
        # Check if the play button is not disabled by default
        self.assertFalse(self.main_screen.ids.play_button.disabled)

    @patch("ui.screens.AUDIO_FILE_PATH", "/path/to/audio/file.mp3")
    def test_play_button_is_disabled_when_path_exists(self):
        self.main_screen.on_enter()

        self.assertFalse(
            self.main_screen.ids.play_button.disabled, "Play button should be disabled"
        )

    def test_on_enter_without_audio_file(self):
        # Call on_enter to update the button state
        self.main_screen.on_enter()

        # Assert that the play button is disabled
        self.assertTrue(
            self.main_screen.ids.play_button.disabled,
            "Play button should be disabled when AUDIO_FILE_PATH is None",
        )

    @patch("ui.screens.AUDIO_FILE_PATH", "/path/to/audio/file.mp3")
    def test_when_button_play_disabled_should_set_info(self):
        self.main_screen.on_enter()

        self.assertEqual(
            self.main_screen.ids.info_label.text, "Selected audio: file.mp3"
        )

    def test_check_button_instance(self):
        self.assertIsInstance(self.main_screen.ids.choose_file_button, Button)
        self.assertIsInstance(self.main_screen.ids.play_button, Button)
        self.assertIsInstance(self.main_screen.ids.read_file_button, Button)

    def test_check_label_instance(self):
        self.assertIsInstance(self.main_screen.ids.info_label, Label)

    def test_check_text_buttons(self):
        self.assertEqual(self.main_screen.ids.choose_file_button.text, "Choose a file")
        self.assertEqual(self.main_screen.ids.play_button.text, "Play")
        self.assertEqual(self.main_screen.ids.read_file_button.text, "Read a file")

    def test_check_label_text(self):
        self.assertEqual(
            self.main_screen.ids.info_label.text,
            "When you choose the file, the button start will be enabled",
        )


if __name__ == "__main__":
    unittest.main()
