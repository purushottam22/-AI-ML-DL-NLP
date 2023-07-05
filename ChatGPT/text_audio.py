import pyttsx3
import speech_recognition as sr


def text_to_speech(data):
    engine = pyttsx3.init()
    engine.say(data)
    engine.runAndWait()


def speech_to_text():
    r = sr.Recognizer()

    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            text_to_speech("Please speak now. you time limit is five seconds")
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level

            # The pause_threshold value is the number of seconds the system will take to recognize the voice after
            # the user has completed their sentence.
            # The timeout value is the maximum number of seconds the system will wait for the user to say something
            # before it throws an OSError exception.
            # The phrase_time_limit value indicates the number of seconds the user can speak. In this case, it is 5.
            # This means that if the user will speak for more than 5 seconds, that speech will not be recognized.

            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source2, duration=0.1)

            # listens for the user's input. Max 5 sec
            while True:
                audio = r.listen(source2, timeout=3, phrase_time_limit=5)
                text_to_speech("Thanks. Processing")
                # Using google to recognize audio
                data = r.recognize_google(audio)
                data = data.lower()
                if len(data) != 10:
                    break
                text_to_speech("Sorry, repeat again")

            print(data)
            return data
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return e
    except sr.UnknownValueError:
        print("unknown error occurred")

        return 0

