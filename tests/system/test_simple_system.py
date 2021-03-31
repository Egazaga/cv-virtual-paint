from mp.main_cam_loop import main_cam
import pandas as pd


class TestSimpleSystem:
    def test_simple_system(self):
        logger = main_cam(phone_cam=False, video_path="tests/images/simple_system_test_30fps.mp4",
                          default_pen_color=[178, 230, 80])
        # logger.save_to_disk("tests/system/simple_system_info.csv")
        right = pd.read_csv("tests/system/simple_system_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)
