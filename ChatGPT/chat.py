import openai
import text_audio
from config import detection_keywords, api_key, model_engine
import random
from ultralytics import YOLO
from object_detection import object_detection


def load_class_list(file_path):
    classes = open(file_path, "r")
    data = classes.read()
    class_list = data.split("\n")
    classes.close()
    return class_list


def color_code(classlist):
    detection_color = []
    for i in range(len(classlist)):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        detection_color.append((r, g, b))
    return detection_color


def load_model():
    model = YOLO("weights/yolov8n.pt", "v8")
    return model


def chatGPT(prompt=None):
    openai.api_key = api_key
    if prompt is None:
        prompt = "Hey chatgpt, can I ask you a question ?"
    print("msg to chatgpt : ", prompt)
    tmp = 0.5

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=tmp,
    )

    response = completion.choices[0].text
    print("response from chatGPT")
    text_audio.text_to_speech(response)


class_list = load_class_list("coco_class.txt")
detection_color = color_code(class_list)
model = load_model()

text_audio.text_to_speech("Hello, Please start. Note : you have 5 sec window to speak")

while True:
    speech = text_audio.speech_to_text()
    keypoints = speech.split()

    if "stop" in keypoints:
        text_audio.text_to_speech("its great to talk with you. Thanks")
        break

    flag = False
    for i in keypoints:
        if i in detection_keywords:
            flag = True

    if flag:
        objects = object_detection(class_list, detection_color, model)
        for item in objects:
            msg = "An " + item + " is detected with a chance of " + str(objects[item]) + " using Yolo model"
            chatGPT(msg)
        text_audio.text_to_speech("An image is saved with object detection")
    else:
        chatGPT(speech)
    text_audio.text_to_speech("ChatGPT done")
