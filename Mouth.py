import pyttsx3


engine = pyttsx3.init()


class Mouth:
    def __init__(self, rate=150, volume=1, voice=1):
        self.rate = rate
        self.volume = volume
        self.voice = voice
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        engine.setProperty('voice', engine.getProperty('voices')[self.voice].id)

    def speak(self, message):
        engine.say(f"{message}")
        engine.runAndWait()
        engine.stop()