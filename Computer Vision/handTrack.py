import cv2
import mediapipe as mp
import time


class handDetector:
    def __init__(self, mode=False, maxHands=2, model_com=1, detectionConf=0.5, trackingConf=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.model_com = model_com
        self.detectionConf = detectionConf
        self.trackingConf = trackingConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_com, self.detectionConf, self.trackingConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPos(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        return lmList


def main(fingerNo=0):
    vid = cv2.VideoCapture(0)

    pTime = 0
    cTime = 0

    detector = handDetector()

    while True:
        success, img = vid.read()
        img = detector.findHands(img)
        lmlist = detector.findPos(img)
        if len(lmlist) != 0:
            print(lmlist[fingerNo])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 255, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main(4)
