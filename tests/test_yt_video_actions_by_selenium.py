import logging
import time
import pytest
from util.base_test import selenium_fixture


logger = logging.getLogger(__name__)

class TestYTVideoActions:
    @pytest.mark.yt_vid_actions
    def test_basic_yt_video_actions(self, selenium_fixture):
        actions = selenium_fixture
        url = "https://www.youtube.com/watch?v=HWeTRgFft1M"
        actions.get_video(url)
        assert int(actions.get_duration()/60) == 6
        # actions.pause()
        actions.play()
        assert actions.is_played()
        actions.pause()
        assert actions.is_paused()
        actions.set_current_time(actions.get_duration()/2)
        time.sleep(5)
        assert int(actions.get_current_time()/60) == 3
        assert actions.get_defaultplayback_rate() == 1
        actions.set_playback_rate(2)
        assert actions.get_playback_rate() == 2
        assert actions.get_resolution() == "480*854"
        # actions.webkit_request_fullscreen()
        # assert actions.is_webkit_displaying_fullscreen()
        # actions.webkit_exit_fullscreen()
        # assert not actions.is_webkit_displaying_fullscreen()
        actions.set_muted("true")
        assert actions.is_muted()
        actions.set_autoplay("true")
        assert actions.is_autoplayenabled()
        actions.set_loop("true")
        assert actions.is_loopenabled()
        #actions.request_pictureinpicture()
