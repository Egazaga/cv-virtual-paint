from mp.main_cam_loop import main_cam
import pandas as pd


class TestSpeedDrawingSystem:
    def test_speed_drawing_system(self):
        logger = main_cam(phone_cam=False,
                          video_path="tests/images/speed_drawing_test_30fps.mp4",
                          default_pen_color=[174, 190, 173])
        # logger.save_to_disk("tests/system/test_speed_drawing_info.csv")
        right = pd.read_csv("tests/system/test_speed_drawing_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)
