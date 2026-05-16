from faster_whisper import WhisperModel # changed from openai whisper to faster which has same accuracy but 4 x faster and less memory
import subprocess
import os
import sys

from database import save_track



#separate the vocals using demucs
#demucs works in the command line so we use the built in python module subprocess


def separate_vocals(audio_path):
    print("Separating vocals...")
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals", "--mp3", audio_path], check = True) # mp3 file

    filename = os.path.splitext(os.path.basename(audio_path))[0]

    vocals_path = os.path.join("separated", "htdemucs", filename, "vocals.mp3") # return an mp3 file, not wav
    return vocals_path


#transcribe the isolated vocals audio file using openai whisper
#it already supports punjabi. 
# However, as expected there will be innacuracies in matras (returned ਸੋਨ instead ਸੌਣ)
# and in spacing (returned ਖਿਆਲਿਕ instead of ਖਿਆਲ ਇਕ)


def transcribe(vocals_path):
    print("Loading Whisper Model...")
    #using the largest model rn, prob should change it cuz my computer cant handle it lol. As seen below
    
    #C:\Users\teghs\Desktop\Code\Bol\venv\Lib\site-packages\whisper\transcribe.py:132: UserWarning: FP16 is not supported on CPU; using FP32 instead
    #warnings.warn("FP16 is not supported on CPU; using FP32 instead")
    #Lyrics saved to testsong_lyrics.txt

    model_size = "medium"

    model = WhisperModel(model_size_or_path=model_size, device="cpu", compute_type="int8")
    

    print("Transcribing...")
    segments, info = model.transcribe(vocals_path, language="pa") # pa = Punjabi

    #progess bar to see if its actually working lol
    result = []
    for segment in segments:
        print(f"[{int(segment.start // 60):02d}:{int(segment.start % 60):02d}] {segment.text.strip()}")
        result.append(segment)

    return result

#save the lyrics into a text file
def save_lyrics(result, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result:
            start = segment.start
            text = segment.text.strip()
            minutes = int(start // 60)
            seconds = int(start % 60)
            f.write(f"[{minutes:02d}:{seconds:02d}] {text}\n") #write when each line starts
            #for some reason in my first test the timings are off, maybe beacause lots of instrumental
            #in the song.
            #Need to try again to see if there is a pattern in the error times.
        print (f"Lyrics saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python transcribe.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    track_name = os.path.splitext(os.path.basename(audio_path))[0]

    vocals_path = separate_vocals(audio_path)
    result = transcribe(vocals_path)

    lyrics_text = ""
    for segment in result:
        lyrics_text += segment.text.strip() + "\n" # type: ignore   

    
    save_lyrics(result, f"{track_name}_lyrics.txt")
    save_track(track_name, None, None, lyrics_text)

