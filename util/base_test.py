from base_objects.vid_obj import vidObj
from base_objects.base_actions.actions import Actions
import pytest
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def selenium_fixture(driver_fixture):
    actions = Actions(driver_fixture)
    yield actions

@pytest.fixture(scope="function")
def opencv_fixture():
    vid_validation = vidObj()
    yield vid_validation