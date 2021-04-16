from mp.main_cam_loop import main_cam
import pandas as pd


class TestSimpleSystem:
    def test_simple_system(self):
        logger = main_cam(phone_cam=False, video_path="tests/images/load_test_30fps.mp4",
                          default_pen_color=[0, 0, 255])
        # logger.save_to_disk("tests/system/simple_system_info.csv")
        right = pd.read_csv("tests/system/load_system_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)
