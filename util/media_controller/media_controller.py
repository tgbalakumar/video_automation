import logging

import cv2
from cap_from_youtube import cap_from_youtube

logger = logging.getLogger(__name__)

class Colors:

    """
    Colors in BGR format
    """

    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    TEAL = (128, 128, 0)
    VIOLET = (238, 130, 238)
    PURPLE = (128, 0, 128)


class OpencvMediaController:

    """
    A wrapper around opencv `VideoCapture` to
    provide media control capabilities
    """

    def __init__(self, source=0, frame_delay_ms=1, jump_interval_ms=10000):

        """
        Constructor, initialize the library

        :param source:              VideoCapture source, camera-index or file path to open
        :param frame_delay_ms:      Opencv waitKey delay, in milliseconds
        :param jump_interval_ms:    Fast-forward/rewind interval, in milliseconds
        """

        # Validate arguments
        if type(source) not in [int, str, cv2.VideoCapture]:
            raise ValueError("'source' must be of the type 'int' or 'str'")

        # Input params
        self.source = source
        self.frame_delay_ms = frame_delay_ms
        self.jump_interval_ms = jump_interval_ms

        self.capture = None
        self.stream_fps = 0
        self.frame_count = 0
        self.num_frames = 0
        self.source_shape = None
        self.is_stream_paused = False
        self._init_video_capture()

    def _init_video_capture(self):
        # Initialize opencv VideoCapture
        self.capture = cv2.VideoCapture(self.source) if type(self.source) in [int, str] else self.source
        if not self.capture.isOpened():
            raise ValueError(f"Failed to open media source: {self.source}")

        # Init frame width and height
        ret, self.current_frame = self.capture.read()
        if not ret:
            return

        # Populate stream params
        self.frame_count += 1
        self.source_shape = self.current_frame.shape[:2]
        self.stream_fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.num_frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.width_of_frames = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height_of_frames = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frames(self):
        """
        Redundant function,
        Implemented for better readability when fetching frames

        :return:    self, the iterator to fetch frames
        """

        return self

    def stop(self):
        """
        - Pause the stream
        - Kill all opened windows
        - Close the camera capture session
        """

        if self.is_stream_paused:
            self.pause()

        # Release opencv resources
        cv2.destroyAllWindows()
        self.capture.release()

    def rewind(self):
        """
        Rewind [seconds (1 second by default) * fps] number of frames
        """

        if self.is_stream_paused:
            return

        self.put_text(f'  <<<  ', fill_color=Colors.PURPLE, font_thickness=2)
        self.frame_count -= (self.stream_fps * (self.jump_interval_ms // 1000))
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_count)

    def fast_forward(self):
        """
        Skip [seconds (1 second by default) * fps] number of frames
        """

        if self.is_stream_paused:
            return

        self.put_text(f'  >>>  ', fill_color=Colors.PURPLE, font_thickness=2)
        if 0 <= self.frame_count < self.num_frames:
            self.frame_count += (self.stream_fps * (self.jump_interval_ms // 1000))
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_count)

    def seek(self):
        if self.is_stream_paused:
            return
        if 0 <= self.frame_count < self.num_frames:
            self.capture.set(cv2.CAP_PROP_POS_MSEC, 3000 * 60)

    def restart(self):
        """
        Restart the stream, Set frame-index to 0
        """

        if self.is_stream_paused:
            return

        self.put_text(f'  Reset  ', fill_color=Colors.RED)
        if 0 <= self.frame_count < self.num_frames:
            self.frame_count = 0
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_count)

    def pause(self):
        """
        Pause Stream
        """

        self.is_stream_paused = not self.is_stream_paused

    def show_frame(self, window_name=''):
        """
        Display the current frame in a window using opencv `imshow`

        :param window_name:     The name of the window, empty by default
        :return:                The window input key if any, else None
        """

        if self.is_stream_paused:
            self.put_text(f'  Paused  ', fill_color=Colors.RED)

        key = cv2.waitKey(self.frame_delay_ms)
        self.command(key)
        cv2.imshow(window_name, self.current_frame)

        return key if key != -1 else None

    def put_text(self, message, position=None, fill_color=Colors.BLACK,
                 text_color=Colors.WHITE, font_thickness=1, is_centered=False):

        """
        Puts text on the screen with a background fill

        :param message:         The message to be displayed
        :param position:        The position of the message, (x, y), defaults to center
        :param fill_color:      The background fill color, defaults to color black
        :param text_color:      The color of the message, defaults to color white
        :param font_thickness:  Thickness of the message, defaults to 1
        :param is_centered:     True if message needs to be centered, False otherwise

        :return:                None
        """

        # Center text if position is not available
        is_centered = is_centered or position is None
        font_family = cv2.FONT_HERSHEY_PLAIN

        if is_centered:
            text_size = cv2.getTextSize(message, font_family, 1, 2)[0]
            text_x = (self.source_shape[1] - text_size[0]) // 2
            text_y = (self.source_shape[0] + text_size[1]) // 2
            position = (text_x, text_y)

        position = (position[0] + 10, position[1] + 20)

        (text_width, text_height) = cv2.getTextSize(message, font_family, 1, font_thickness)[0]
        text_box = ((position[0] - 10, position[1] - 10),
                    (position[0] + text_width - 10, position[1] + text_height - 35))

        cv2.rectangle(self.current_frame, text_box[0], text_box[1], fill_color, cv2.FILLED)
        cv2.putText(self.current_frame, message, text_box[0], font_family,
                    1, text_color, font_thickness)

    def command(self, key):
        """
        Handle input from opencv waitKey

        :param key:     The input Key
        :return:        None
        """

        if key == ord('q'):
            self.stop()
        elif key == ord('a'):
            self.rewind()
        elif key == ord('d'):
            self.fast_forward()
        elif key == ord('r'):
            self.restart()
        elif key == ord('s'):
            self.seek()
        elif key == 32:
            # 32 is the space-bar
            self.pause()
        elif key == ord('c'):
            print(f"The total duration of the video is: {self.num_frames/self.stream_fps/60} minutes")
            print(f"Resolution of the video is : {self.width_of_frames} * {self.height_of_frames}")
            print(f"Current position of the video is : {self.capture.get(cv2.CAP_PROP_POS_MSEC)/1000} seconds")
            duration = self.num_frames/self.stream_fps/60
            resolution = f"{self.width_of_frames} * {self.height_of_frames}"
            current_pos = self.capture.get(cv2.CAP_PROP_POS_MSEC)/1000
            return duration, resolution, current_pos

    def __next__(self):

        # If frame paused, return current frame
        if self.is_stream_paused:
            return self.current_frame

        # Read the next frame
        ret, frame = self.capture.read()
        if not ret or frame is None:
            raise StopIteration

        self.current_frame = frame
        self.frame_count += 1
        return frame

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
