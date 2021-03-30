from mp.drawing import Drawing
from utils.motion_analyser import MotionAnalyser


class TestMovingAndScalingCombinations:
    def test_mr_sd(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 1000), 5)
        ma.analyse((500, 1000), 5)
        ma.analyse((0, 0), 0)
        ma.analyse((0, 216), 0)
        print(drawing.view_corner)
        assert drawing.view_corner == (670, 1080)

    def test_sd_ml(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 0), 0)
        ma.analyse((0, 216), 0)
        ma.analyse((0, 1000), 5)
        ma.analyse((500, 1000), 5)
        print(drawing.view_corner)
        assert drawing.view_corner == (45, 1080)

    def test_su_mr(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((0, 216), 0)
        ma.analyse((0, 0), 0)
        ma.analyse((0, 1000), 5)
        ma.analyse((500, 1000), 5)
        print(drawing.view_corner)
        assert drawing.view_corner == (1295, 1080)

    def test_mrd_su(self):
        drawing = Drawing(1920, 1080)
        ma = MotionAnalyser(1080, 1920, drawing)
        ma.analyse((500, 500), 5)
        ma.analyse((0, 0), 5)
        ma.analyse((0, 0), 0)
        ma.analyse((0, 216), 0)
        print(drawing.view_corner)
        assert drawing.view_corner == (2880, 1620)
