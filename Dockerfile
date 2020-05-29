FROM python:3.7

WORKDIR /usr/src/app

ADD requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt --extra-index-url=https://www.piwheels.org/simple

COPY . .

CMD [ "python", "./src/main.py", "--display", "ssd1322", "--width", "256", "--height", "64", "--interface", "spi" ]
# CMD [ "python", "./src/main.py", "--display", "pygame", "--width", "256", "--height", "64" ]