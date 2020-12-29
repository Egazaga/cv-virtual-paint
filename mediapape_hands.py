import cv2
import mediapipe as mp
from imutils.video import FPS


def n_fingers(hand_landmarks):
    lm = hand_landmarks.landmark
    n = (lm[4].x > lm[3].x) + (lm[8].y < lm[7].y) + (lm[12].y < lm[11].y) + (lm[16].y < lm[15].y) + (lm[20].y < lm[19].y)
    print(n)


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
address = "http://192.168.1.193:8080/video"
cap.open(address)
fps = FPS().start()

while cap.isOpened():
    fps.update()
    success, image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for mh in results.multi_handedness:
            label = mh.classification[0].label
            if label == "Left\r":
                n_fingers(results.multi_hand_landmarks[0])
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

fps.stop()
print(fps.fps())
hands.close()
cap.release()
