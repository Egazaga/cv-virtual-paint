import cv2


def count_fingers(frame, detector, hand="Left"):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame.flags.writeable = False
    results = detector.process(frame)
    frame.flags.writeable = True
    n_fingers_l, center_l = None, None

    if results.multi_hand_landmarks:
        for mh, lm in zip(results.multi_handedness, results.multi_hand_landmarks):
            label = mh.classification[0].label
            lm = lm.landmark
            if label == hand:
                n_fingers_l = (lm[4].x > lm[3].x) + (lm[8].y < lm[7].y) + (lm[12].y < lm[11].y) + (
                        lm[16].y < lm[15].y) + (lm[20].y < lm[19].y)
                sh = frame.shape
                center_l = (lm[9].x * sh[1], lm[9].y * sh[0])
    return n_fingers_l, center_l
