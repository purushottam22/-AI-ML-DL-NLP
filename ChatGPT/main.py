import random
from ultralytics import YOLO
from object_detection import object_detection
import text_audio
from config import detection_keywords


classes = open("coco_class.txt", "r")
data = classes.read()
class_list = data.split("\n")
classes.close()

detection_color = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_color.append((r, g, b))

# loading yolo model
model = YOLO("weights/yolov8n.pt", "v8")

# text_audio.text_to_speech("Hello, Please start : ")
speech = text_audio.speech_to_text()
keypoints = speech.split()

flag = False
for i in keypoints:
    if i in detection_keywords:
        flag = True

if flag :
    objects = object_detection(class_list, detection_color, model)
    for item in objects:
        msg = item + "detected with accuracy of " + str(objects[item])
        text_audio.text_to_speech(msg)

text_audio.text_to_speech("An image is saved")