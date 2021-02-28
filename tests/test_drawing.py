from unittest import TestCase
from mp.drawing import Drawing
import numpy as np
import cv2

class TestDrawing(TestCase):
    def test_set_pen_color_edge(self):
        drawing = Drawing(1920, 1080)
        color = np.array([0, 0, 0])
        drawing.set_pen_color(color)
        self.assertTrue(np.array_equal(drawing.pen_color_range[0], np.zeros(3)))
        self.assertTrue(np.array_equal(drawing.pen_color_range[1], color + drawing.d_color_range))

    def test_set_pen_color_1(self):
        drawing = Drawing(1920, 1080)
        color = np.array([120, 150, 150])
        drawing.set_pen_color(color)
        color = cv2.cvtColor(np.array([[color]], dtype="uint8"), cv2.COLOR_BGR2HSV)[0, 0]  # brg to hsv
        self.assertTrue(np.array_equal(drawing.pen_color_range[0], color - drawing.d_color_range))
        self.assertTrue(np.array_equal(drawing.pen_color_range[1], color + drawing.d_color_range))


    def test_find_pen(self):
        # drawing = Drawing(1920, 1080)
        # white_color = np.array([255, 255, 225])
        # drawing.pen_color_range = np.array([white_color - drawing.d_color_range, white_color + drawing.d_color_range])
        # drawing.find_pen()
        self.fail()

    def test_process_frame(self):
        self.fail()

    def test_move(self):
        self.fail()

    def test_scale(self):
        self.fail()
