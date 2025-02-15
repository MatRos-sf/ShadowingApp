import unittest
from unittest.mock import MagicMock

import pytest
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from ui.screens.play_audio_screen import PlayAudioScreen


# @pytest.mark.usefixtures("play_audio_screen")
class TestPlayAudioScreen(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup_play_audio_screen(self):
        self.play_audio_screen = PlayAudioScreen(name="test_screen")
        self.play_audio_screen.ids = {
            "title": Label(),
            "progress_bar": Slider(),
            "current_time": Label(),
            "time_stamp_info": Label(),
            "total_time": Label(),
            "reverse_button": Button(),
            "pause_button": Button(),
            "play_button": Button(),
            "time_stamp_button": Button(),
            "next_button": Button(),
            "back_button": Button(),
            "save_button": Button(),
        }

    def test_initial_values(self):
        """Verify the initial values"""
        self.assertIsNone(self.play_audio_screen.sound)
        self.assertIsNone(self.play_audio_screen.update_event)
        self.assertEqual(self.play_audio_screen.current_position, 0)
        self.assertEqual(self.play_audio_screen._time_stamp, [0])
        self.assertEqual(self.play_audio_screen.time_stamp_index, 0)

    def test_widgets_exist(self):
        """Verify that all widgets were created"""
        self.assertIsNotNone(self.play_audio_screen.ids["title"])
        self.assertIsNotNone(self.play_audio_screen.ids["progress_bar"])
        self.assertIsNotNone(self.play_audio_screen.ids["current_time"])
        self.assertIsNotNone(self.play_audio_screen.ids["time_stamp_info"])
        self.assertIsNotNone(self.play_audio_screen.ids["total_time"])
        self.assertIsNotNone(self.play_audio_screen.ids["reverse_button"])
        self.assertIsNotNone(self.play_audio_screen.ids["pause_button"])
        self.assertIsNotNone(self.play_audio_screen.ids["play_button"])
        self.assertIsNotNone(self.play_audio_screen.ids["time_stamp_button"])
        self.assertIsNotNone(self.play_audio_screen.ids["next_button"])
        self.assertIsNotNone(self.play_audio_screen.ids["back_button"])
        self.assertIsNotNone(self.play_audio_screen.ids["save_button"])
        self.assertEqual(len(self.play_audio_screen.ids), 12)

    def test_type_of_widgets(self):
        """Verify the type of widgets"""
        self.assertIsInstance(self.play_audio_screen.ids["title"], Label)
        self.assertIsInstance(self.play_audio_screen.ids["progress_bar"], Slider)
        self.assertIsInstance(self.play_audio_screen.ids["current_time"], Label)
        self.assertIsInstance(self.play_audio_screen.ids["time_stamp_info"], Label)
        self.assertIsInstance(self.play_audio_screen.ids["total_time"], Label)
        self.assertIsInstance(self.play_audio_screen.ids["reverse_button"], Button)
        self.assertIsInstance(self.play_audio_screen.ids["pause_button"], Button)
        self.assertIsInstance(self.play_audio_screen.ids["play_button"], Button)
        self.assertIsInstance(self.play_audio_screen.ids["time_stamp_button"], Button)
        self.assertIsInstance(self.play_audio_screen.ids["next_button"], Button)
        self.assertIsInstance(self.play_audio_screen.ids["back_button"], Button)
        self.assertIsInstance(self.play_audio_screen.ids["save_button"], Button)

    def test_play_sound(self):
        """Test playing sound"""
        self.play_audio_screen.sound = MagicMock()
        self.play_audio_screen.play()
        self.play_audio_screen.sound.play.assert_called_once()
        self.assertIsNotNone(self.play_audio_screen.update_event)

    def test_pause_sound(self):
        """Test pausing sound"""
        self.play_audio_screen.sound = MagicMock(state="play")
        self.play_audio_screen.pause()
        self.play_audio_screen.sound.stop.assert_called_once()
        self.assertIsNone(self.play_audio_screen.update_event)
        self.assertEqual(self.play_audio_screen.ids["pause_button"].disabled, True)

    def test_set_time_stamp(self):
        """Test setting a time stamp"""
        self.play_audio_screen.sound = MagicMock()
        self.play_audio_screen.sound.get_pos.return_value = 10
        self.play_audio_screen.set_time_stamp()
        self.assertIn(10, self.play_audio_screen._time_stamp)
        self.assertEqual(self.play_audio_screen.time_stamp_index, 1)

    def test_navigate_next(self):
        """Test navigating to the next time stamp"""
        self.play_audio_screen.sound = MagicMock()
        self.play_audio_screen._time_stamp = [0, 10, 20]
        self.play_audio_screen.time_stamp_index = 0
        self.play_audio_screen.navigate(1)
        self.assertEqual(self.play_audio_screen.time_stamp_index, 1)

    def test_navigate_reverse(self):
        """Test navigating to the previous time stamp"""
        self.play_audio_screen.sound = MagicMock()
        self.play_audio_screen._time_stamp = [0, 10, 20]
        self.play_audio_screen.time_stamp_index = 2
        self.play_audio_screen.navigate(-1)
        self.assertEqual(self.play_audio_screen.time_stamp_index, 1)

    def test_update_progress_bar(self):
        """Test updating the progress bar"""
        self.play_audio_screen.sound = MagicMock()
        self.play_audio_screen.sound.get_pos.return_value = 5
        self.play_audio_screen.sound.length = 10
        self.play_audio_screen.update_progress_bar(0.1)
        self.assertEqual(self.play_audio_screen.ids["progress_bar"].value, 5)
        self.assertEqual(self.play_audio_screen.ids["current_time"].text, "00:05")

    def test_format_time(
        self,
    ):
        """Test formatting time"""
        formatted_time = self.play_audio_screen._format_time(125)
        self.assertEqual(formatted_time, "02:05")
