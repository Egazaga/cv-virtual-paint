from unittest import TestCase
from mp.main_cam_loop import _count_fingers
import cv2
import mediapipe as mp


class Test(TestCase):
    def test__count_fingers_5_fingers(self):
        img = cv2.flip(cv2.imread("images/hand_5.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 5)
        self.assertAlmostEqual(center_l[0], 677.3, places=1)
        self.assertAlmostEqual(center_l[1], 1016.5, places=1)

    def test__count_fingers_4_fingers(self):
        img = cv2.flip(cv2.imread("images/hand_4.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 4)
        self.assertAlmostEqual(center_l[0], 712.6, places=1)
        self.assertAlmostEqual(center_l[1], 1030.8, places=1)

    def test__count_fingers_3_fingers(self):
        img = cv2.flip(cv2.imread("images/hand_3.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 3)
        self.assertAlmostEqual(center_l[0], 748.6, places=1)
        self.assertAlmostEqual(center_l[1], 1065.5, places=1)

    def test__count_fingers_2_fingers(self):
        img = cv2.flip(cv2.imread("images/hand_2.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 2)
        self.assertAlmostEqual(center_l[0], 805.3, places=1)
        self.assertAlmostEqual(center_l[1], 1124.8, places=1)

    def test__count_fingers_1_fingers(self):
        img = cv2.flip(cv2.imread("images/hand_1.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 1)
        self.assertAlmostEqual(center_l[0], 827.2, places=1)
        self.assertAlmostEqual(center_l[1], 1141.1, places=1)

    def test__count_fingers_0_fingers(self):
        img = cv2.flip(cv2.imread("images/hand_0.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 0)
        self.assertAlmostEqual(center_l[0], 732.0, places=1)
        self.assertAlmostEqual(center_l[1], 1005.2, places=1)

    def test__count_fingers_5_fingers_far(self):
        img = cv2.flip(cv2.imread("images/hand_far.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 5)
        self.assertAlmostEqual(center_l[0], 466.6, places=1)
        self.assertAlmostEqual(center_l[1], 756.6, places=1)

    def test__count_fingers_splitted(self):
        img = cv2.flip(cv2.imread("images/hand_spider.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 3)
        self.assertAlmostEqual(center_l[0], 780.8, places=1)
        self.assertAlmostEqual(center_l[1], 1146.4, places=1)

    def test__count_fingers_shadow(self):
        img = cv2.flip(cv2.imread("images/hand_shadow.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertIsNone(n_fingers_l)
        self.assertIsNone(center_l)

    def test__count_fingers_hand_and_shadow(self):
        img = cv2.flip(cv2.imread("images/hand_with_shadow.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        self.assertEqual(n_fingers_l, 5)
        self.assertAlmostEqual(center_l[0], 953.9, places=1)
        self.assertAlmostEqual(center_l[1], 1101.6, places=1)
