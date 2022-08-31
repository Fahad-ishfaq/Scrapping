import speech_recognition as sr
from pydub import AudioSegment

filename = "audio/audio.mp3"

dst = "audio/test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(filename)
sound.export(dst, format="wav")

r = sr.Recognizer()
with sr.AudioFile(dst) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)