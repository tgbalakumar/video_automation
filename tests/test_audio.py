from pytube import YouTube
import pytest
import logging

logger = logging.getLogger(__name__)


class TestAudio:
    @pytest.mark.audio
    def test_yt_audio(self):
        video = YouTube("https://www.youtube.com/shorts/eT890bLLrjk")
        audio = video.streams.filter(only_audio=True, file_extension='mp4')[0]
        audio.download()
        #print(SequenceMatcher(None, open("Parrot.mp4", "rb").read(), open("audio_output/highway.mp4", "rb").read()).ratio())
        print(open("tests/input/Parrot.mp4", "rb").read() == open("Parrot Photobombs Highway Traffic Cam Shorts.mp4", "rb").read())

