from mp.main_cam_loop import main_cam
import pandas as pd


class TestHighFpsSystem:
    def test_high_fps_system(self):
        logger = main_cam(phone_cam=False,
                          video_path="tests/images/system_test_120fps.mp4",
                          default_pen_color=[174, 190, 173])
        # logger.save_to_disk("tests/system/test_high_fps_info.csv")
        right = pd.read_csv("tests/system/test_high_fps_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)
