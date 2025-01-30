import unittest

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from ui.screens import ReadFileScreen


class TestFileChooser(unittest.TestCase):
    def setUp(self):
        self.file_chooser = ReadFileScreen(name="test_screen")

    def test_widgets_exist(self):
        """Verify that all widgets was created"""
        self.assertIsNotNone(self.file_chooser.ids.info_label)
        self.assertIsNotNone(self.file_chooser.ids.scroll_view)
        self.assertIsNotNone(self.file_chooser.ids.chose_file)
        self.assertIsNotNone(self.file_chooser.ids.button_back)
        self.assertIsNotNone(self.file_chooser.ids.button_choose)

    def test_type_of_widgets(self):
        """Verify the type of widgets"""
        self.assertIsInstance(self.file_chooser.ids.info_label, Label)
        self.assertIsInstance(self.file_chooser.ids.scroll_view, ScrollView)
        self.assertIsInstance(self.file_chooser.ids.chose_file, Label)
        self.assertIsInstance(self.file_chooser.ids.button_back, Button)
        self.assertIsInstance(self.file_chooser.ids.button_choose, Button)
