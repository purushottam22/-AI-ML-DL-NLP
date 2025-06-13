import cv2
import time
import numpy as np
import hadnTrack as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 648, 488

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime = 0
pTime = 0

detector = htm.handDetector(detectionConf=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
vol = 0
volBar = 400
volper = 0

minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPos(img, draw=False)

    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volper = np.interp(length, [50, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        if length <= 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (10, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 255, 255), 2)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
