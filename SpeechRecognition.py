import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
print(sr.Microphone.list_microphone_names())
with mic as source:
    r.adjust_for_ambient_noise(source)
    while 1 == 1:
        # try:
            print("[listening...]")
            audio = r.listen(source)
            print("[analyzing...]")
            voice = r.recognize_sphinx(audio, show_all=True).hyp()
            print(str(voice.best_score) + " : " + voice.hypstr)
        #except:
            print("")

