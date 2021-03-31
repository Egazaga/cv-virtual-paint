import cv2
import numpy as np

from mp.drawing import Drawing


class TestSetPenColor:
    def test_set_pen_color_edge(self):
        drawing = Drawing(1920, 1080)
        color = np.array([0, 0, 0])
        drawing.set_pen_color(color)
        assert np.array_equal(drawing.pen_color_range[0], np.zeros(3))
        assert np.array_equal(drawing.pen_color_range[1], color + drawing.d_color_range)

    def test_set_pen_color_1(self):
        drawing = Drawing(1920, 1080)
        color = np.array([120, 150, 150])
        drawing.set_pen_color(color)
        color = cv2.cvtColor(np.array([[color]], dtype="uint8"), cv2.COLOR_BGR2HSV)[0, 0]
        assert np.array_equal(drawing.pen_color_range[0], color - drawing.d_color_range)
        assert np.array_equal(drawing.pen_color_range[1], color + drawing.d_color_range)

    # def test_find_pen(self):
    #     # drawing = Drawing(1920, 1080)
    #     # white_color = np.array([255, 255, 225])
    #     # drawing.pen_color_range = np.array([white_color - drawing.d_color_range, white_color + drawing.d_color_range])
    #     # drawing.find_pen()
    #     self.fail()


class TestProcessFrame:
    def test_process_frame_general_blue(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=200, action="Blue")
        for x in range(300, 400):
            assert drawing.canvas[x + 1080, x + 1920].all() == np.array([255, 0, 0]).all()

    def test_process_frame_general_yellow(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Yellow")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Yellow")
        drawing.process_frame(frame=frame, x=300, y=400, area=200, action="Yellow")
        for y in range(300, 400):
            assert drawing.canvas[300 + 1080, y + 1920].all() == np.array([0, 255, 255]).all()

    def test_process_frame_general_width(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Yellow")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Yellow")
        drawing.process_frame(frame=frame, x=300, y=400, area=200, action="Yellow")
        for x in range(300 - 13, 300 + 13):
            for y in range(300, 400):
                assert drawing.canvas[x + 1080, y + 1920].all() == np.array([0, 255, 255]).all()

    def test_process_frame_no_pen(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action=None)
        assert drawing.ex_action == None
        assert drawing.ex_pen_pos == (0, 0)

    def test_process_frame_action_changed(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=5, y=5, area=200, action="Yellow")
        drawing.process_frame(frame=frame, x=10, y=10, area=200, action="Blue")
        assert drawing.ex_action == "Blue"
        assert drawing.ex_pen_pos == (1930, 1090)

    def test_process_frame_no_previous_pen(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Blue")
        drawing.process_frame(frame=frame, x=10, y=10, area=200, action="Blue")
        print(drawing.ex_pen_pos)
        assert drawing.ex_pen_pos == (1930, 1090)


class TestScale:
    def test_scale_up(self):
        drawing = Drawing(1920, 1080)
        drawing.scale(1080 / 10)
        assert drawing.scale_factor == 1.25

    def test_scale_down(self):
        drawing = Drawing(1920, 1080)
        drawing.scale(- 1080 / 10)
        assert drawing.scale_factor == 0.75

    def test_scale_out_of_bounds_high(self):
        drawing = Drawing(1920, 1080)
        drawing.scale_factor = 3
        drawing.scale(10)
        assert drawing.scale_factor == 3

    def test_scale_out_of_bounds_low(self):
        drawing = Drawing(1920, 1080)
        drawing.scale_factor = 0.5
        drawing.scale(-10)
        assert drawing.scale_factor == 0.5

    def test_scale_near_canvas_bound(self):
        drawing = Drawing(1920, 1080)
        drawing.view_corner = (1920 * 2, 1080 * 2)
        drawing.scale(1080 / 10)
        assert drawing.view_corner == (3360, 1890)
