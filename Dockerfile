FROM python:3.7-slim

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc-dev

ADD requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt --extra-index-url=https://www.piwheels.org/simple

COPY . .

RUN apt-get remove -y gcc
RUN apt-get -y autoremove

CMD [ "python", "./src/main.py", "--display", "ssd1322", "--width", "256", "--height", "64", "--interface", "spi" ]