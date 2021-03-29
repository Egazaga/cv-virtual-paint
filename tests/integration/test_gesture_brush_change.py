import numpy as np

from mp.drawing import Drawing
from utils.motion_analyser import MotionAnalyser


class TestGestureBrushDetection:
    def test_none_gesture_brush(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")

        # Frame 1
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action=None)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action=None)
        # Frame 2
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action=None)

        assert (drawing.canvas == np.array([0, 0, 0])).all()

    def test_same_gesture_brush(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")

        # Frame 1
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        # Frame 2
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")

        assert (drawing.canvas[1080 + 100, 1920 + 100] == np.array([255, 0, 0])).all()

    def test_change_gesture(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")

        # Frame 1
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        # Frame 2
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Erase")
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Erase")

        assert (drawing.canvas[1080 + 100, 1920 + 100] == np.array([0, 0, 0])).all()

    def test_change_brush(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")

        # Frame 1
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        # Frame 2
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Green")

        assert (drawing.canvas[1080 + 100, 1920 + 100] == np.array([255, 0, 0])).all()

    def test_change_gesture_brush(self):
        drawing = Drawing(1920, 1080)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")

        # Frame 1
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        drawing.process_frame(frame=frame, x=100, y=100, area=2, action="Blue")
        # Frame 2
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erase")
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erase")

        assert (drawing.canvas[1080 + 100, 1920 + 100] == np.array([255, 0, 0])).all()
