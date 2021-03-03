from unittest import TestCase
from utils.motion_analyser import MotionAnalyser
from mp.drawing import Drawing


class TestMotionAnalyser(TestCase):
    def test_analyse_gesture_none(self):
        # Setup
        width = 1920
        height = 1080
        pos = 1.23, 3.55
        gesture = None
        drawing = Drawing(width, height)
        ma = MotionAnalyser(width, height, drawing)

        # Act
        ma.analyse(pos, gesture)
        ma.analyse(pos, gesture)

        # Check
        exp_gesture = gesture
        exp_pos = 0, 0
        exp_total_dx = 0
        exp_total_dy = 0
        self.assertEqual(exp_gesture, ma.ex_gesture)
        self.assertAlmostEqual(exp_pos, ma.ex_pos)
        self.assertAlmostEqual(exp_total_dx, ma.total_dx)
        self.assertAlmostEqual(exp_total_dy, ma.total_dy)

    def test_analyse_gesture_change_on_start(self):
        # Setup
        width = 1920
        height = 1080
        pos = 0, 0
        gesture = 1
        drawing = Drawing(width, height)
        ma = MotionAnalyser(width, height, drawing)

        # Act
        ma.analyse(pos, gesture)

        # Check
        exp_gesture = gesture
        exp_pos = pos
        exp_total_dx = 0
        exp_total_dy = 0
        self.assertEqual(exp_gesture, ma.ex_gesture)
        self.assertAlmostEqual(exp_pos, ma.ex_pos)
        self.assertAlmostEqual(exp_total_dx, ma.total_dx)
        self.assertAlmostEqual(exp_total_dy, ma.total_dy)

    def test_analyse_gesture_same(self):
        # Setup
        width = 1920
        height = 1080
        pos = 0, 0
        gesture = 1
        drawing = Drawing(width, height)
        ma = MotionAnalyser(width, height, drawing)

        # Act
        ma.analyse(pos, gesture)
        ma.analyse(pos, gesture)
        ma.analyse(pos, gesture)

        # Check
        exp_gesture = gesture
        exp_pos = pos
        exp_total_dx = pos[0]
        exp_total_dy = pos[1]
        self.assertEqual(exp_gesture, ma.ex_gesture)
        self.assertAlmostEqual(exp_pos, ma.ex_pos)
        self.assertAlmostEqual(exp_total_dx, ma.total_dx)
        self.assertAlmostEqual(exp_total_dy, ma.total_dy)

    def test_analyse_gesture_change(self):
        # Setup
        width = 1920
        height = 1080
        pos = 0, 0
        gesture_1 = 1
        gesture_2 = 2
        gesture_3 = 3
        drawing = Drawing(width, height)
        ma = MotionAnalyser(width, height, drawing)

        # Act
        ma.analyse(pos, gesture_1)
        ma.analyse(pos, gesture_1)
        ma.analyse(pos, gesture_2)
        ma.analyse(pos, gesture_2)
        ma.analyse(pos, gesture_1)
        ma.analyse(pos, gesture_3)

        # Check
        exp_gesture = gesture_3
        exp_pos = pos
        exp_total_dx = pos[0]
        exp_total_dy = pos[0]
        self.assertEqual(exp_gesture, ma.ex_gesture)
        self.assertAlmostEqual(exp_pos, ma.ex_pos)
        self.assertAlmostEqual(exp_total_dx, ma.total_dx)
        self.assertAlmostEqual(exp_total_dy, ma.total_dy)

    def test_analyse_gesture_same_in_motion(self):
        # Setup
        width = 1920
        height = 1080
        pos_1 = 0, 0
        pos_2 = 1, 6
        pos_3 = 5, 4
        pos_4 = 2, 4
        pos_5 = 11, 0
        gesture = 1
        drawing = Drawing(width, height)
        ma = MotionAnalyser(width, height, drawing)

        # Act
        ma.analyse(pos_1, gesture)
        ma.analyse(pos_2, gesture)
        ma.analyse(pos_3, gesture)
        ma.analyse(pos_4, gesture)
        ma.analyse(pos_5, gesture)

        # Check
        exp_gesture = gesture
        exp_pos = pos_5
        exp_total_dx = 11
        exp_total_dy = 0
        self.assertEqual(exp_gesture, ma.ex_gesture)
        self.assertAlmostEqual(exp_pos, ma.ex_pos)
        self.assertAlmostEqual(exp_total_dx, ma.total_dx)
        self.assertAlmostEqual(exp_total_dy, ma.total_dy)

    def test_analyse_gesture_change_in_motion(self):
        # Setup
        width = 1920
        height = 1080
        pos_1 = 0, 0
        pos_2 = 1, 6
        pos_3 = 5, 4
        pos_4 = 2, 4
        pos_5 = 11, 0
        gesture_1 = 1
        gesture_2 = 2
        gesture_3 = 3
        drawing = Drawing(width, height)
        ma = MotionAnalyser(width, height, drawing)

        # Act
        ma.analyse(pos_1, gesture_1)
        ma.analyse(pos_2, gesture_1)
        ma.analyse(pos_3, gesture_2)
        ma.analyse(pos_3, gesture_2)
        ma.analyse(pos_4, gesture_1)
        ma.analyse(pos_5, gesture_3)

        # Check
        exp_gesture = gesture_3
        exp_pos = pos_5
        exp_total_dx = 0
        exp_total_dy = 0
        self.assertEqual(exp_gesture, ma.ex_gesture)
        self.assertAlmostEqual(exp_pos, ma.ex_pos)
        self.assertAlmostEqual(exp_total_dx, ma.total_dx)
        self.assertAlmostEqual(exp_total_dy, ma.total_dy)
