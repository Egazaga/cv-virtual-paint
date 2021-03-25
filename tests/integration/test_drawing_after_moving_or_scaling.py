import numpy as np

from mp.drawing import Drawing
from utils.motion_analyser import MotionAnalyser


class TestDrawingAfterMovingOrScaling:
    def test_draw_after_moving_left(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        ma.analyse((0, 1000), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        ma.analyse((500, 1000), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=200, action="Blue")
        print(drawing.view_corner)
        for x in range(300, 400):
            assert (drawing.canvas[x + 1080, x + 670] == np.array([255, 0, 0])).all()

    def test_draw_after_moving_right(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        ma.analyse((500, 1000), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        ma.analyse((0, 1000), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        print(drawing.view_corner)
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=200, action="Blue")
        for x in range(300, 400):
            print(np.array([255, 0, 0]).all())
            assert (drawing.canvas[x + 1080, x + 3170] == np.array([255, 0, 0])).all()

    def test_draw_after_moving_up(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        ma.analyse((0, 300), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        ma.analyse((0, 0), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        print(drawing.view_corner)
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=200, action="Blue")
        for x in range(300, 400):
            print(np.array([255, 0, 0]).all())
            assert (drawing.canvas[x + 1830, x + 1920] == np.array([255, 0, 0])).all()

    def test_draw_after_moving_down(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        ma.analyse((0, 0), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        ma.analyse((0, 300), 5)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Erasing")
        print(drawing.view_corner)
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=200, action="Blue")
        for x in range(300, 400):
            print(np.array([255, 0, 0]).all())
            assert (drawing.canvas[x + 330, x + 1920] == np.array([255, 0, 0])).all()

    def test_draw_after_scaling_up(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        ma.analyse((0, 0), 0)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Green")
        ma.analyse((0, 216), 0)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Green")
        print(drawing.view_corner, drawing.scale_factor)
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=200, action="Blue")
        for x in range(300, 400):
            assert (drawing.canvas[int(x * 1.5 + 1080), int(x * 1.5 + 1920)] == np.array([255, 0, 0])).all()

    def test_draw_after_scaling_down(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        ma.analyse((0, 216), 0)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Green")
        ma.analyse((0, 0), 0)
        drawing.process_frame(frame=frame, x=None, y=None, area=None, action="Green")
        print(drawing.view_corner, drawing.scale_factor)
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=300, area=200, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=200, action="Blue")
        print(np.where(drawing.canvas > 0))
        for x in range(300, 400):
            assert (drawing.canvas[int(x * 0.5 + 1080), int(x * 0.5 + 1920)] == np.array([255, 0, 0])).all()
