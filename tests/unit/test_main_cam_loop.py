import cv2
import mediapipe as mp

from mp.main_cam_loop import _count_fingers


class TestCountFingers:
    def test__count_fingers_5_fingers(self):
        img = cv2.flip(cv2.imread("tests/images/hand_5.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 5
        assert round(abs(center_l[0] - 677.3), 1) == 0
        assert round(abs(center_l[1] - 1016.5), 1) == 0

    def test__count_fingers_4_fingers(self):
        img = cv2.flip(cv2.imread("tests/images/hand_4.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 4
        assert round(abs(center_l[0] - 712.6), 1) == 0
        assert round(abs(center_l[1] - 1030.8), 1) == 0

    def test__count_fingers_3_fingers(self):
        img = cv2.flip(cv2.imread("tests/images/hand_3.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 3
        assert round(abs(center_l[0] - 748.6), 1) == 0
        assert round(abs(center_l[1] - 1065.5), 1) == 0

    def test__count_fingers_2_fingers(self):
        img = cv2.flip(cv2.imread("tests/images/hand_2.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 2
        assert round(abs(center_l[0] - 805.3), 1) == 0
        assert round(abs(center_l[1] - 1124.8), 1) == 0

    def test__count_fingers_1_fingers(self):
        img = cv2.flip(cv2.imread("tests/images/hand_1.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 1
        assert round(abs(center_l[0] - 827.2), 1) == 0
        assert round(abs(center_l[1] - 1141.1), 1) == 0

    def test__count_fingers_0_fingers(self):
        img = cv2.flip(cv2.imread("tests/images/hand_0.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 0
        assert round(abs(center_l[0] - 732.0), 1) == 0
        assert round(abs(center_l[1] - 1005.2), 1) == 0

    def test__count_fingers_5_fingers_far(self):
        img = cv2.flip(cv2.imread("tests/images/hand_far.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 5
        assert round(abs(center_l[0] - 466.6), 1) == 0
        assert round(abs(center_l[1] - 756.6), 1) == 0

    def test__count_fingers_splitted(self):
        img = cv2.flip(cv2.imread("tests/images/hand_spider.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 3
        assert round(abs(center_l[0] - 780.8), 1) == 0
        assert round(abs(center_l[1] - 1146.4), 1) == 0

    def test__count_fingers_shadow(self):
        img = cv2.flip(cv2.imread("tests/images/hand_shadow.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l is None
        assert center_l is None

    def test__count_fingers_hand_and_shadow(self):
        img = cv2.flip(cv2.imread("tests/images/hand_with_shadow.jpeg", cv2.IMREAD_COLOR), 1)
        detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        n_fingers_l, center_l = _count_fingers(img, detector)
        assert n_fingers_l == 5
        assert round(abs(center_l[0] - 953.9), 1) == 0
        assert round(abs(center_l[1] - 1101.6), 1) == 0
