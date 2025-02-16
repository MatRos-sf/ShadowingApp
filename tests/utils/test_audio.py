import tempfile
import time
from pathlib import Path

import pytest
from pydub.generators import Sine

from models.session_manager import AudioSession
from utils.audio import AudioPlayer, TimeStampManager


@pytest.fixture
def sample_audio_session():
    return AudioSession(1, "Session 1", Path("/old/path"), [1.0, 2.0], 120, 30, 5)


class TestTimeStampManager:
    @pytest.mark.parametrize(
        "audio_session, expected",
        [
            (
                AudioSession(1, "Session 1", Path("/old/path"), [0.1, 0.2], 120, 30, 5),
                0.2,
            ),
            (AudioSession(1, "Session 1", Path("/old/path"), [], 120, 30, 5), 0),
        ],
    )
    def test_should_return_current_stamp(self, audio_session, expected):
        time_stamp_instance = TimeStampManager(audio_session)
        assert time_stamp_instance.stamp == expected

    @pytest.mark.parametrize(
        "audio_session, expected",
        [
            (
                AudioSession(1, "Session 1", Path("/old/path"), [0.1, 0.2], 120, 30, 5),
                [0.1, 0.2],
            ),
            (AudioSession(1, "Session 1", Path("/old/path"), [], 120, 30, 5), [0]),
        ],
    )
    def test_should_return_time_stamp_list(self, audio_session, expected):
        time_stamp_instance = TimeStampManager(audio_session)
        assert time_stamp_instance.time_stamp_list == expected

    @pytest.mark.parametrize("value", [1, 3, 10])
    def test_should_not_set_new_time_stamp_index_when_value_is_bigest_than_list(
        self, value, sample_audio_session
    ):
        instance = TimeStampManager(sample_audio_session)
        index = instance.time_stamp_index
        instance.time_stamp_index += value
        assert index == instance.time_stamp_index

    def test_should_add_new_time_stamp(self, sample_audio_session):
        instance = TimeStampManager(sample_audio_session)
        initial_length = len(instance.time_stamp_list)
        new_time_stamp = 3.0
        result = instance.add_time_stamp(new_time_stamp)
        assert result is True
        assert len(instance.time_stamp_list) == initial_length + 1
        assert new_time_stamp in instance.time_stamp_list

    def test_should_not_add_duplicate_time_stamp(self, sample_audio_session):
        instance = TimeStampManager(sample_audio_session)
        initial_length = len(instance.time_stamp_list)
        duplicate_time_stamp = 2
        result = instance.add_time_stamp(duplicate_time_stamp)
        assert result is False
        assert len(instance.time_stamp_list) == initial_length

    @pytest.mark.parametrize(
        "index, expected_range", [(0, (1.0, 2.0)), (1, (2.0, None))]
    )
    def test_should_return_correct_range(
        self, sample_audio_session, index, expected_range
    ):
        instance = TimeStampManager(sample_audio_session)
        instance.time_stamp_index = index
        assert instance.range() == expected_range


class TestAudioPlayer:
    def setup_method(self, test_method):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            self.file_path = Path(tmp.name)

        self.sine_wave = Sine(440).to_audio_segment(duration=10000)
        self.sine_wave.export(str(self.file_path), format="mp3")
        self.player = AudioPlayer(self.file_path)

    def test_audio_player_load(self):
        assert self.player.sound is not None
        assert int(self.player.sound_length) == 10

    def test_play(self):
        self.player.play()
        assert self.player.sound.state == "play"
        time.sleep(2)
        pos = self.player.get_position()
        assert self.player.current_position < pos

    def test_audio_player_pause(self):
        self.player.play()
        self.player.pause()

        pos_after_pause = self.player.get_position()
        assert pos_after_pause > 0

    def test_audio_player_cleanup(self):
        self.player.cleanup()
        assert self.player.sound is None or self.player.sound.unload
