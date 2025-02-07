import unittest

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from ui.screens.play_audio_screen import PlayAudioScreen


class TestFileChooser(unittest.TestCase):
    def setUp(self):
        self.file_chooser = PlayAudioScreen(name="test_screen")

    def test_initial_values(self):
        """Verify the initial values"""
        self.assertIsNone(self.file_chooser.sound)
        self.assertIsNone(self.file_chooser.update_event)
        self.assertEqual(self.file_chooser.current_position, 0)

    def test_widgets_exist(self):
        """Verify that all widgets was created"""
        self.assertIsNotNone(self.file_chooser.ids.title)
        self.assertIsNotNone(self.file_chooser.ids.progress_bar)
        self.assertIsNotNone(self.file_chooser.ids.current_time)
        self.assertIsNotNone(self.file_chooser.ids.time_stamp_info)
        self.assertIsNotNone(self.file_chooser.ids.total_time)
        self.assertIsNotNone(self.file_chooser.ids.reverse_button)
        self.assertIsNotNone(self.file_chooser.ids.pause_button)
        self.assertIsNotNone(self.file_chooser.ids.play_button)
        self.assertIsNotNone(self.file_chooser.ids.time_stamp_button)
        self.assertIsNotNone(self.file_chooser.ids.next_button)
        self.assertIsNotNone(self.file_chooser.ids.back_button)
        self.assertIsNotNone(self.file_chooser.ids.save_button)
        self.assertEqual(len(self.file_chooser.ids), 12)

    def test_type_of_widgets(self):
        """Verify the type of widgets"""
        self.assertIsInstance(self.file_chooser.ids.title, Label)
        self.assertIsInstance(self.file_chooser.ids.progress_bar, Slider)
        self.assertIsInstance(self.file_chooser.ids.current_time, Label)
        self.assertIsInstance(self.file_chooser.ids.time_stamp_info, Label)
        self.assertIsInstance(self.file_chooser.ids.total_time, Label)
        self.assertIsInstance(self.file_chooser.ids.reverse_button, Button)
        self.assertIsInstance(self.file_chooser.ids.pause_button, Button)
        self.assertIsInstance(self.file_chooser.ids.play_button, Button)
        self.assertIsInstance(self.file_chooser.ids.time_stamp_button, Button)
        self.assertIsInstance(self.file_chooser.ids.next_button, Button)
        self.assertIsInstance(self.file_chooser.ids.back_button, Button)
        self.assertIsInstance(self.file_chooser.ids.save_button, Button)
