import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone () as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source,
                                  timeout=5,
                                  phrase_time_limit=5)

    try:
        command = recognizer.recognize_google(audio)

        print("You said:", command)

        return command.lower()
    
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")

        return ""
    except sr.RequestError:

        print("Internet problem.")

        return ""   
    