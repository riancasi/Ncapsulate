FROM python:3.9-slim

COPY requirements.txt /

#RUN apk add python3-dev cmake ffmpeg gcc build-base
RUN apt-get update -qq
RUN apt-get install -y --no-install-recommends build-essential wget openssh-client graphviz-dev pkg-config git-core openssl libssl-dev libffi-dev libpng-dev libpq-dev curl ffmpeg
RUN apt-get clean

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip install -r /requirements.txt
RUN python3 -m spacy download en_core_web_md

COPY . /app/
WORKDIR /app

CMD ["python", "app.py"]
