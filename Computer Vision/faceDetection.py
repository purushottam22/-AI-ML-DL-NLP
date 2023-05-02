import cv2
import mediapipe as mp
import time


class faceDetection:
    def __init__(self, min_detection_confidence=0.5, model_selection=0):
        self.min_detection_confidence = min_detection_confidence
        self.model_selection = model_selection

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.min_detection_confidence, self.model_selection)

    def faceDetect(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        return img

    def faceBox(self, img, draw=True):
        lrlist = []

        if self.results.detections:
            for id, detect in enumerate(self.results.detections):

                bboxc = detect.location_data.relative_bounding_box

                ih, iw, ic = img.shape
                bbox = int(bboxc.xmin * iw), int(bboxc.ymin * ih), int(bboxc.width * iw), int(bboxc.height * ih)
                lrlist.append([id, int(bboxc.xmin * iw), int(bboxc.ymin * ih), int(bboxc.width * iw),
                               int(bboxc.height * ih)])
                if draw:
                    cv2.rectangle(img, bbox, (255, 0, 255), 2)

                    cv2.putText(img, str(int(detect.score[0] * 100)), (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                                3, (255, 255, 255), 2)
        return lrlist


def main():
    vid = cv2.VideoCapture(0)

    pTime = 0
    cTime = 0

    fd = faceDetection()
    while True:
        success, img = vid.read()
        img = fd.faceDetect(img)
        lrlist = fd.faceBox(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 255, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
