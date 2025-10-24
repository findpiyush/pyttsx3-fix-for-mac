import pyttsx3

engine = pyttsx3.init()

engine.say("I want pizza")
engine.runAndWait()

print("hello")

voices = engine.getProperty('voices')
for voice in voices:
    print("ID:", voice.id)
    print("Name:", voice.name)
    print("Languages:", voice.languages)
    print("Gender:", voice.gender)
    print("Age:", voice.age)
    print("")