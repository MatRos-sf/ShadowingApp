import unittest
from pathlib import Path

from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label

from ui.screens.file_chooser import FileChooser


class TestFileChooser(unittest.TestCase):
    def setUp(self):
        self.file_chooser = FileChooser(name="test_screen")

    def test_widgets_exist(self):
        """Verify that all widgets was created"""
        self.assertIsNotNone(
            self.file_chooser.ids.file_chooser, "FileChooser does not exist"
        )
        self.assertIsNotNone(
            self.file_chooser.ids.selected_label, "Selected Label does not exist"
        )
        self.assertIsNotNone(
            self.file_chooser.ids.choose_button, "Choose Button does not exist"
        )
        self.assertIsNotNone(
            self.file_chooser.ids.cancel_button, "Cancel Button does not exist"
        )

    def test_type_of_widgets(self):
        """Verify the type of widgets"""
        self.assertIsInstance(self.file_chooser.ids.file_chooser, FileChooserIconView)
        self.assertIsInstance(self.file_chooser.ids.selected_label, Label)
        self.assertIsInstance(self.file_chooser.ids.choose_button, Button)
        self.assertIsInstance(self.file_chooser.ids.cancel_button, Button)

    def test_file_chooser_path_should_be_home(self):
        """Verify the initial path of the FileChooserIconView"""
        self.assertEqual(self.file_chooser.ids.file_chooser.path, str(Path.home()))

    def test_selected(self):
        """Verify the selected method"""
        self.file_chooser.selected(["/path/to/audio/file.mp3"])
        self.assertEqual(
            self.file_chooser.ids.selected_label.text,
            "Selected audio: /path/to/audio/file.mp3",
        )

    def test_choose_button_should_be_disabled(self):
        """Verify the choose button is disabled by default"""
        self.assertTrue(self.file_chooser.ids.choose_button.disabled)
