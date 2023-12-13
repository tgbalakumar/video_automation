import pytest, logging
from util.base_test import opencv_fixture

logger = logging.getLogger(__name__)

class TestObjectRelevanceInVideo:

    @pytest.mark.find_object_relevance
    @pytest.mark.parametrize("url, objects", [("https://www.youtube.com/shorts/yiYLEpRkS_U", {"sports ball", "person", "tennis racket"}),
                                              ("https://www.youtube.com/shorts/BsCRHvZwHXA", {'truck', 'traffic light', 'stop sign'}),
                                              ("https://www.youtube.com/shorts/s8PfCAo1pZQ", {'giraffe', 'frisbee', 'elephant'}),
                                              ("https://www.youtube.com/shorts/zQhjxZhIgG8", {'person', 'apple', 'diningtable'}),
                                              ("https://youtube.com/shorts/DNFa-5vtUzE?feature=shared", {'knife', 'person', 'pizza'})])
    def test_objects_relevance_in_video(self, opencv_fixture, url, objects):
        vid_validation = opencv_fixture
        logger.info(f"objects available are {objects}")
        assert vid_validation.yolo_video().find_relevance(url) == objects
