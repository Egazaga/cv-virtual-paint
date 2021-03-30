import numpy as np
import math

from mp.drawing import Drawing
from utils.motion_analyser import MotionAnalyser

class TestDrawingAfterColorChanged:
    # G
    #   G       
    #     G   
    #       B
    #         B
    #           B
    def test_draw_after_color_green_to_blue(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 0), 5)
        ma.analyse((0, 300), 5)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Blue")
        drawing.process_frame(frame=frame, x=350, y=350, area=196, action="Blue")
        for x in range(300, int(350 - 14 / math.sqrt(2))):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([0, 255, 0])).all()
        for x in range(int(350 - 14 / math.sqrt(2)) + 1, 400):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([255, 0, 0])).all()

    # G           B
    #   G       B
    #     G   B
    #       B
    #     B   G
    #   B       G
    def test_draw_after_color_green_to_blue_cross(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 0), 5)
        ma.analyse((0, 300), 5)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=300, area=196, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=300, area=196, action="Blue")
        drawing.process_frame(frame=frame, x=300, y=400, area=196, action="Blue")
        #cross top-left part
        for x in range(300, int(350 - 14 / math.sqrt(2))):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([0, 255, 0])).all(), x
        #cross intersection part
        for x in range(int(350 - 14 / math.sqrt(2)) + 1, int(350 + 14 / math.sqrt(2))):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([255, 0, 0])).all(), x
        #after cross intersection, must be same as topleft
        for x in range(int(350 + 14 / math.sqrt(2)) + 2, 400):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([0, 255, 0])).all(), x

    # GGGGGGGG -> EEEEEEEE
    def test_draw_after_color_erase_drawn(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 0), 5)
        ma.analyse((0, 300), 5)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Erasing")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Erasing")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Erasing")
        for x in range(300, 400):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([0, 0, 0])).all()

    # G
    #   G       
    #     G   
    #       G
    #         G
    #           G
    # ---->
    # G
    #   G       
    #     G   
    #       E
    #         E
    #           E
    def test_draw_after_color_erase_drawn_partially(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 0), 5)
        ma.analyse((0, 300), 5)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=12, action="Erasing")
        drawing.process_frame(frame=frame, x=400, y=400, area=12, action="Erasing")
        drawing.process_frame(frame=frame, x=350, y=350, area=12, action="Erasing")
        
        for x in range(300, 350 - int(math.sqrt(int(math.sqrt(12) * 2.0) * 2.0)) - 1):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([0, 255, 0])).all(), x
        for x in range(350 - int(math.sqrt(int(math.sqrt(12) * 2.0) * 2.0)), 400):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([0, 0, 0])).all(), x


    # G
    #   G       blk
    #     G   blk
    #       blk
    #    blk   blue
    # blk        blue
    def test_draw_after_color_green_then_blue_and_cross_black(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 0), 5)
        ma.analyse((0, 300), 5)
        frame = np.zeros((1080, 1920, 3), dtype="uint8")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=300, y=300, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Green")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=400, area=196, action="Blue")
        drawing.process_frame(frame=frame, x=350, y=350, area=196, action="Blue")
        drawing.process_frame(frame=frame, x=400, y=300, area=196, action="Black")
        drawing.process_frame(frame=frame, x=400, y=300, area=196, action="Black")
        drawing.process_frame(frame=frame, x=300, y=400, area=196, action="Black")
        #cross top-left part
        for x in range(300, int(350 - 14 / math.sqrt(2))):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([0, 255, 0])).all(), x
        #cross intersection part
        for x in range(int(350 - 14 / math.sqrt(2)) + 1, int(350 + 14 / math.sqrt(2))):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([255, 255, 255])).all(), x
        #after cross intersection, must be same as topleft
        for x in range(int(350 + 14 / math.sqrt(2)) + 2, 400):
            assert (drawing.canvas[x + 330, x + 1920] == np.array([255, 0, 0])).all(), x
    