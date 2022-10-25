# import library
import speech_recognition as sr
import Mouth
# Initialize recognizer class (for recognizing the speech)
tongue = Mouth.Mouth()


def take_user_input():
    recognizer = sr.Recognizer()
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        tongue.speak("Start Talking")
        audio_text = recognizer.listen(source)
        tongue.speak("Time over, thank you")

        try:
            # using google speech recognition
            msg = recognizer.recognize_google(audio_text)
        except:
            msg = "could not process the audio"
    return msg
