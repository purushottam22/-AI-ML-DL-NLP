import cv2
import time
import poseEstimatoin


# cap = cv2.VideoCapture(0)

cTime = 0
pTime = 0
pose = poseEstimatoin.poseDetection()
while True:
    img = cv2.imread("test.png")
    img = pose.findPose(img, draw=False)
    lmlist = pose.findPosition(img, draw=False)

    if len(lmlist) != 0:
        angle = pose.findAngle(img, 12, 24, 26)
        # pose.findAngle(img, 11, 23, 25)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)