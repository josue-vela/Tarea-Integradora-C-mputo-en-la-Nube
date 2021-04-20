FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get -y install python3-dev
RUN apt-get -y install python3-pip 
RUN pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 8420

CMD [ "python3", "main.py"]
