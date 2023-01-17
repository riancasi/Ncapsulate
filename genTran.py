from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import subprocess
import json

def generate_transcript():
    sample_rate=16000
    model = Model("model")
    rec = KaldiRecognizer(model, sample_rate)

    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                sys.argv[1],
                                '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                                stdout=subprocess.PIPE)

    path = sys.argv[2]
    with open(f"{path}/output.txt", "w") as f:
        result = ""
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                f.write(res["text"] + "\n")
            else:
                pass

if __name__ == "__main__":
    generate_transcript()
