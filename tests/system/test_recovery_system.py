from mp.main_cam_loop import main_cam
import pandas as pd


class TestSimpleSystem:
    def test_simple_system(self):
        imgs_paths = ["tests/images/hand_0.jpeg",
                      "tests/images/hand_1.jpeg",
                      None,
                      None,
                      "tests/images/hand_2.jpeg",
                      "tests/images/hand_3.jpeg"]
        logger = main_cam(phone_cam=False, imgs_paths=imgs_paths, default_pen_color=[178, 230, 80])
        # logger.save_to_disk("tests/system/recovery_info.csv")
        right = pd.read_csv("tests/system/recovery_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)
