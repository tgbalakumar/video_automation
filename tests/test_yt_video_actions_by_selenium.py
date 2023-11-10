import logging
import time
import pytest
from util.base_test import base_fixture


logger = logging.getLogger(__name__)

class TestYTVideoActions:
    @pytest.mark.yt_vid_actions
    def test_basic_yt_video_actions(self, base_fixture):
        actions, vid_validation = base_fixture
        url = "https://www.youtube.com/watch?v=HWeTRgFft1M"
        actions.get_video(url)
        assert int(actions.get_duration()/60) == 6
        # actions.pause()
        actions.play()
        assert actions.is_played()
        actions.pause()
        assert actions.is_paused()
        actions.set_current_time(actions.get_duration()/2)
        time.sleep(10)
        assert int(actions.get_current_time()/60) == 3