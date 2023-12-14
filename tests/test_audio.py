from pytube import YouTube
import pytest
import logging
from util.base_test import yaml_fixture

logger = logging.getLogger(__name__)


class TestAudio:
    @pytest.mark.audio
    @pytest.mark.common
    def test_yt_audio(self, yaml_fixture):
        video = YouTube(yaml_fixture["tests"]["audio"]["url"])
        audio = video.streams.filter(only_audio=True, file_extension='mp4')[0]
        audio.download()
        #print(SequenceMatcher(None, open("Parrot.mp4", "rb").read(), open("audio_output/highway.mp4", "rb").read()).ratio())
        print(open(yaml_fixture["tests"]["audio"]["input"], "rb").read() == open(yaml_fixture["tests"]["audio"]["output"], "rb").read())

