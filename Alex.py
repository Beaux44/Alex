import speech_recognition as sr, pyttsx3 as tts, time
from concurrent.futures import ThreadPoolExecutor as Executor
engine = tts.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

mic = sr.Microphone()
recognizer = sr.Recognizer()

with mic as source:
    with Executor(max_workers=1) as exe:
        start = time.time()
        exe.submit(recognizer.adjust_for_ambient_noise, (source, 10))
        say("Hello, my name is Alex. I am currently assessing the ambient noise level of your current environment. Please wait while I do this.")
        time.sleep(10 - min(10, max(0, time.time() - start)))
    say("Thank you for waiting, I am ready now. Please speak loudly and clearly.")
    while True:
        try:
            audio = recognizer.listen(source, phrase_time_limit=2)
            words = recognizer.recognize_sphinx(audio)
        except sr.UnknownValueError:
            continue
        print(words)
        if words == "hey alex":
            say("I'm Listening.")
            try:
                audio = recognizer.listen(source, timeout=10)
                words = recognizer.recognize_sphinx(audio)
            except (sr.WaitTimeoutError, sr.UnknownValueError) as e:
                if type(e) == sr.UnknownValueError:
                    say("Sorry, I didn't catch that.")
                continue
            print(words)
            say(words)
