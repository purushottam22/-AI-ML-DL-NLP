import cv2
import text_audio
from config import frame_wid, frame_height
from collections import defaultdict


def object_detection(class_list, detection_color, model):
    all_detected_object = defaultdict(int)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        text_audio.text_to_speech("Sorry!   can not open camera")
        exit()

    # while True:

    ret, frame = cap.read()

    if not ret:
        text_audio.text_to_speech("Sorry, not able to receive image")
        # break
        return

    frame = cv2.resize(frame, (frame_wid, frame_height))

    cv2.imwrite("images/img.png", frame)

    detect_params = model.predict(source="images/img.png", conf=0.5, save=True)

    DP = detect_params[0].numpy()

    if len(DP) != 0:
        for i in range(len(detect_params[0])):

            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                detection_color[int(clsID)],
                3,
            )

            # Display class name and confidence
            font = cv2.FONT_HERSHEY_COMPLEX

            cv2.putText(
                frame,
                class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                (int(bb[0]), int(bb[1]) - 10),
                font,
                1,
                (255, 255, 255),
                2,
            )

            # text_audio.text_to_speech("detected object is " + class_list[int(clsID)])
            all_detected_object[class_list[int(clsID)]] = max(int(conf*100),
                                                              all_detected_object[class_list[int(clsID)]])
        # cv2.imshow('object_detection', frame)

        # if cv2.waitKey(1) == ord('q'):
        #     text_audio.text_to_speech("Thankyou!")
        #     break

    cap.release()
    cv2.destroyAllWindows()

    return all_detected_object
