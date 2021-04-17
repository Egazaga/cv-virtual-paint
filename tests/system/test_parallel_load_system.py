from mp.main_cam_loop import main_cam
import pandas as pd

from multiprocessing import Pool
from multiprocessing import cpu_count

stop_loop = 0

def exit_child(x, y):
    global stop_loop
    stop_loop = 1
    pass

def f(x):
    global stop_loop
    while not stop_loop:
        x * x / 3 * 85165 + 100 - 125.87
    pass


class TestSimpleSystem:
    def test_simple_system(self):
        logger = main_cam(phone_cam=False, video_path="tests/images/load_test_30fps.mp4",
                          default_pen_color=[0, 0, 255])
        procs = cpu_count()
        pool = Pool(procs)
        pool.map(f, range(procs * 4))
        exit_child(0, 0)
        right = pd.read_csv("tests/system/load_system_info.csv")
        pd.testing.assert_frame_equal(logger.memory, right)
