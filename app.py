from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import string, random
import os
import subprocess
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/static/<path:path>")
def css(path):
    return send_from_directory("static", path)

@app.route("/upload", methods=['GET', 'POST'])
def upload_post():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            path = generateRandomDir()
            filename = secure_filename(file.filename)
            file.save(os.path.join(path, filename))

            full_file_path = f"{path}/{filename}"
            audio_name = file.filename.split(".")[0]
            full_audio_path = f"{path}/{audio_name}"
           
            os.system(f"python3 convertToMp3.py {full_file_path} {full_audio_path}")
            print(f"EXECUTING ____________ python3 genTran.py {full_audio_path}.mp3 {path}")
            os.system(f"python3 genTran.py {full_audio_path}.mp3 {path}")

            transcript = ""
            full_txt_path = f"{path}/output.txt"
            with open(f"{full_txt_path}", "r") as f:
                transcript = f.read()
                print(transcript)

            summary = ""
            os.system(f"python3 genSum.py {full_txt_path} {path}")
            with open(f"{path}/summary.txt", "r") as f:
                summary = f.read()
                print(summary)
            
            res = {"transcript": transcript, "summary": summary}

            return render_template("output.html", transcript=res['transcript'], summary=res['summary']) 
        else:
            return "<p>format not allowed</p>"
    else:
        return render_template("index.html")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp4'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generateRandomDir():
    letters = string.ascii_letters
    temp_dir = "".join(random.choice(letters) for i in range(12))
    final_dir = f"videos/{temp_dir}"
    os.makedirs(final_dir)
    return final_dir


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='0.0.0.0')
