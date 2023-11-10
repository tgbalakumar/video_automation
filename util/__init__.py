from .media_controller.media_controller import OpencvMediaController
from .yolo.yolo_video import YoloVideo

media_control = OpencvMediaController
yolo_video = YoloVideo

__all__ = ['media_control', 'yolo_video']