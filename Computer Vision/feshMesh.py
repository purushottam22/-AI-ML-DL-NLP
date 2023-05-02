import cv2
import mediapipe as mp
import time


class FeshMesh:
    def __init__(self, static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.static_image_mode, self.max_num_faces, self.refine_landmarks,
                                                 self.min_detection_confidence)
        self.drawSpecs = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)

    def feshMeshDetect(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)

        return img

    def detectBoundry(self, img, draw=True):
        lmlist = []

        if self.results.multi_face_landmarks:
            for facelm in self.results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(img, facelm, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpecs,
                                           self.drawSpecs)
                for id, lm in enumerate(facelm.landmark):
                    ih, iw, ic = img.shape
                    cx, cy = int(lm.x * iw), int(lm.y * ih)
                    lmlist.append([id, cx, cy])
        return lmlist


def main():
    vid = cv2.VideoCapture(0)

    pTime = 0
    cTime = 0
    fm = FeshMesh()
    while True:
        success, img = vid.read()
        img = fm.feshMeshDetect(img)
        lmlist = fm.detectBoundry(img)
        print(lmlist)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 255, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
