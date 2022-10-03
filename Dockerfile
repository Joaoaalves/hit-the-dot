FROM python:3.10.7-slim-buster

WORKDIR /htd

RUN apt-get update
RUN apt-get install python3-dev -y
RUN apt install build-essential -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "uwsgi",  "./htd.ini"]