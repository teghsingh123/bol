import whisper
import subprocess
import os
import sys



#separate the vocals usiing demucs
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

    model = whisper.load_model("large-v3") 
    

    print("Transcribing...")
    result = model.transcribe(vocals_path, language="pa") # pa = Punjabi

    return result


#save the lyrics into a text file
def save_lyrics(result, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            text = segment["text"].strip()
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

    save_lyrics(result, f"{track_name}_lyrics.txt")

