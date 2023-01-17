import os
import sys

def start():
    if len(sys.argv) < 3:
        print("error")
    else:
        video_name = sys.argv[1]
        audio_name = sys.argv[2]
        command = f"ffmpeg -i {video_name} {audio_name}.mp3"
        os.system(command)

if __name__ == "__main__":
   start() 
