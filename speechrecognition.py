import speech_recognition as sr 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import wave



class SpeechRecognizer:
    def extractAudio(self, videoName: str, videoFormat: str, audioFormat: str):
        inputName = videoName + videoFormat
        outputName = videoName + audioFormat
        clip = mp.VideoFileClip(inputName) 
        clip.audio.write_audiofile(outputName, fps = 22050)

    def extractText(self, name: str, audioFormat: str, textFormat: str):
        r = sr.Recognizer()
        inputName = name + audioFormat
        outputName = name + textFormat
        audio = sr.AudioFile(inputName)
        with audio as source:
            audio_file = r.record(source)
            result = r.recognize_google(audio_file, language="ru-RU")
        
        # exporting the result 
        with open(outputName,mode ='w') as file: 
            file.write("Recognized Speech:") 
            file.write("\n") 
            file.write(result) 
            print("ready!")
    
    def cutAudio(self, name: str, audioFormat: str):
        # times between which to extract the wave from
        start = 0.0 # seconds
        end = 180.0 # seconds

        initialName = name + audioFormat
        targetName = name + "-cut" + audioFormat

        # file to extract the snippet from
        with wave.open(initialName, "rb") as infile:
            # get file data
            nchannels = infile.getnchannels()
            sampwidth = infile.getsampwidth()
            framerate = infile.getframerate()
            # set position in wave to start of segment
            infile.setpos(int(start * framerate))
            # extract data
            data = infile.readframes(int((end - start) * framerate))

        # write the extracted data to a new file
        with wave.open(targetName, 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(framerate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)       



# videoName = "2.15. Растворители. Праймеры и дегидраторы"
# recognizer = SpeechRecognizer()
# recognizer.extractAudio(videoName=videoName, videoFormat=".mp4", audioFormat=".wav")


# recognizer.cutAudio(name=videoName, audioFormat=".mp3")
# recognizer.extractText(name=videoName, audioFormat=".mp3", textFormat="txt")
# recognizer.cutAudio(name=videoName)
