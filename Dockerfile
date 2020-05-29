FROM python:3.7

WORKDIR /usr/src/app

# Dependencies for the PyGame emulator
# From https://stackoverflow.com/a/56454086
RUN apt update -y
RUN apt install python3.7-dev python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev -y

COPY requirements.txt ./

# PyGame needs up to date pip setuptools to build
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main.py", "--display", "pygame", "--width", "256", "--height", "64" ]