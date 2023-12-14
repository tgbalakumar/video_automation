import logging
import pytest
import time, cv2
from cap_from_youtube import cap_from_youtube
from util.base_test import opencv_fixture, yaml_fixture

logger = logging.getLogger(__name__)

class TestMediaControlsOpenCV:

    @pytest.mark.media_controls_standalone
    @pytest.mark.common
    def test_media_controls_for_standalone_video(self, opencv_fixture, yaml_fixture):
        vid_validation = opencv_fixture
        progress, progress2 , progress3= False, False, False
        with vid_validation.media_control(source=yaml_fixture["tests"]["media_control"]["standalone"]["source"]) as omc:
            for _ in omc.get_frames():
                omc.show_frame()
                #logger.info(omc.capture.get(cv2.CAP_PROP_POS_MSEC)/1000)
                if 5 < omc.capture.get(cv2.CAP_PROP_POS_MSEC)/1000 < 6:
                    before_frame_count = omc.frame_count
                    omc.fast_forward()
                    time.sleep(5)
                    after_frame_count = omc.frame_count
                    assert (after_frame_count - before_frame_count)/omc.stream_fps == yaml_fixture["tests"]["media_control"]["standalone"]["duration"]
                logger.info(omc.frame_count)
                if int(omc.frame_count) == 1000 and not progress:
                    before_frame_count = omc.frame_count
                    omc.rewind()
                    time.sleep(5)
                    after_frame_count = omc.frame_count
                    assert round((before_frame_count - after_frame_count) / omc.stream_fps) == yaml_fixture["tests"]["media_control"]["standalone"]["duration"]
                    progress = True
                if int(omc.frame_count) == 1500 and not progress2:
                    omc.restart()
                    time.sleep(5)
                    assert omc.frame_count == 0
                    progress2 = True
                if int(omc.frame_count) == 500 and progress2:
                    before_frame_count = omc.frame_count
                    omc.pause()
                    after_frame_count = omc.frame_count
                    assert before_frame_count == after_frame_count
                    progress3 = True
                if int(omc.frame_count) == 600 and progress3:
                    assert int(omc.num_frames/omc.stream_fps) == 101
                    assert f"{omc.width_of_frames} * {omc.height_of_frames}" == yaml_fixture["tests"]["media_control"]["standalone"]["resolution"]
                    omc.stop()

    @pytest.mark.media_controls_yt
    @pytest.mark.common
    def test_media_controls_for_yt_video(self, opencv_fixture, yaml_fixture):
        vid_validation = opencv_fixture
        progress, progress2, progress3 = False, False, False
        url = yaml_fixture["tests"]["media_control"]["yt"]["source"]
        cap = cap_from_youtube(url, '1080p')
        with vid_validation.media_control(source=cap) as omc:
            for _ in omc.get_frames():
                omc.show_frame()
                # logger.info(omc.capture.get(cv2.CAP_PROP_POS_MSEC)/1000)
                if 5 < omc.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000 < 6:
                    before_frame_count = omc.frame_count
                    omc.fast_forward()
                    time.sleep(5)
                    after_frame_count = omc.frame_count
                    assert (after_frame_count - before_frame_count) / omc.stream_fps == yaml_fixture["tests"]["media_control"]["yt"]["duration"]
                logger.info(omc.frame_count)
                if int(omc.frame_count) == 1000 and not progress:
                    before_frame_count = omc.frame_count
                    omc.rewind()
                    time.sleep(5)
                    after_frame_count = omc.frame_count
                    assert round((before_frame_count - after_frame_count) / omc.stream_fps) == yaml_fixture["tests"]["media_control"]["yt"]["duration"]
                    progress = True
                if int(omc.frame_count) == 1500 and not progress2:
                    omc.restart()
                    time.sleep(5)
                    assert omc.frame_count == 0
                    progress2 = True
                if int(omc.frame_count) == 500 and progress2:
                    before_frame_count = omc.frame_count
                    omc.pause()
                    after_frame_count = omc.frame_count
                    assert before_frame_count == after_frame_count
                    progress3 = True
                if int(omc.frame_count) == 600 and progress3:
                    assert int(omc.num_frames / omc.stream_fps / 60) == 3
                    assert f"{omc.width_of_frames} * {omc.height_of_frames}" == yaml_fixture["tests"]["media_control"]["yt"]["resolution"]
                    omc.stop()




