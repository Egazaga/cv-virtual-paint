import numpy as np
import cv2
from imutils.video import FPS
from utils.motion_analyser import MotionAnalyser


def get_class_with_max_confidence(outputs, conf_threshold):
    max_tuple = (0, 0, 0)
    for i in outputs:
        part = i[:, 5:]  # get confidences of classes
        index = np.unravel_index(np.argmax(part), part.shape)  # index tuple of max confidence in output layer
        conf = part[index]
        if conf > max_tuple[0] and conf > conf_threshold:
            classID = index[1]
            center = i[index[0]][0:2]
            max_tuple = (conf, classID, center)

    if max_tuple[0] == 0:  # didn't find bb
        return None, None, None
    else:
        return max_tuple


def make_prediction(net, layer_names, image, conf_threshold):
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(layer_names)
    return get_class_with_max_confidence(outputs, conf_threshold)


if __name__ == '__main__':
    labels = open('model/_darknet.labels').read().strip().split('\n')
    cfg, weights = 'model/custom-yolov4-detector.cfg', 'model/yolov4-hand-gesture.weights'
    net = cv2.dnn.readNetFromDarknet(cfgFile=cfg, darknetModel=weights)

    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    cap = cv2.VideoCapture(0)
    address = "http://192.168.1.193:8080/video"
    cap.open(address)
    fps = FPS().start()
    W = cap.get(3)
    H = cap.get(4)
    ma = MotionAnalyser(W, H)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print('Video file finished.')
            break
        frame = cv2.flip(frame, 1)

        conf, class_id, center = make_prediction(net, layer_names, frame, conf_threshold=0.6)
        if class_id is None:
            text = "None"
        else:
            text = labels[class_id]
            center = (int(center[0] * W), int(center[1] * H))
            cv2.circle(frame, center, 35, [0, 255, 20], thickness=-1)
            motion = ma.analyse(center, gesture=text)
            if motion is not None:
                print(motion)

        cv2.putText(frame, text=text, org=(30, 100), fontFace=0, fontScale=3, color=(0, 255, 20), thickness=5)

        fps.update()
        cv2.imshow('Cam', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    fps.stop()
    print("Mean fps for detection:", round(fps.fps(), 2))
    cap.release()
