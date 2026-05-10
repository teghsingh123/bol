import whisper
import subprocess
import os
import sys

def separate_vocals(audio_path):
    print("Separating vocals...")
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals", "--mp3", audio_path], check = True)

    filename = os.path.splitext(os.path.basename(audio_path))[0]

    vocals_path = os.path.join("separated", "htdemucs", filename, "vocals.mp3")
    return vocals_path


def transcribe(vocals_path):
    print("Loading Whisper Model...")
    model = whisper.load_model("large-v3")

    print("Transcribing...")
    result = model.transcribe(vocals_path, language="pa") # pa = Punjabi

    return result

def save_lyrics(result, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            text = segment["text"].strip()
            minutes = int(start // 60)
            seconds = int(start % 60)
            f.write(f"[{minutes:02d}:{seconds:02d}] {text}\n")
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

