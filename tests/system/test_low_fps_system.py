from mp.main_cam_loop import main_cam
import pandas as pd


class TestLowFpsSystem:
    def test_low_10fps_system(self):
        logger = main_cam(phone_cam=False,
                          video_path="/Users/levkargalov/Desktop/cv-virtual-paint/tests/images/simple_system_test_10fps.mp4",
                          default_pen_color=[174, 190, 173])
        # logger.save_to_disk("/Users/levkargalov/Desktop/cv-virtual-paint/tests/system/test_low_10fps_info.csv")
        right = pd.read_csv("/Users/levkargalov/Desktop/cv-virtual-paint/tests/system/test_low_10fps_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)


    def test_low_5fps_system(self):
        logger = main_cam(phone_cam=False,
                          video_path="/Users/levkargalov/Desktop/cv-virtual-paint/tests/images/simple_system_test_5fps.mp4",
                          default_pen_color=[174, 190, 173])
        # logger.save_to_disk("/Users/levkargalov/Desktop/cv-virtual-paint/tests/system/test_low_5fps_info.csv")
        right = pd.read_csv("/Users/levkargalov/Desktop/cv-virtual-paint/tests/system/test_low_5fps_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)


    def test_low_1fps_system(self):
        logger = main_cam(phone_cam=False,
                          video_path="/Users/levkargalov/Desktop/cv-virtual-paint/tests/images/simple_system_test_1fps.mp4",
                          default_pen_color=[174, 190, 173])
        # logger.save_to_disk("/Users/levkargalov/Desktop/cv-virtual-paint/tests/system/test_low_1fps_info.csv")
        right = pd.read_csv("/Users/levkargalov/Desktop/cv-virtual-paint/tests/system/test_low_1fps_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)