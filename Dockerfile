FROM continuumio/anaconda3:2022.10

ADD . /code
WORKDIR /code

# https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "app.py" ]