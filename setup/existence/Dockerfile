FROM ubuntu:20.04

WORKDIR /home

RUN apt update
RUN apt install python3 pip -y
RUN pip3 install SPARQLWrapper

ADD *.py ./
ADD *.sh ./
COPY .dockerignore .*.tmp ./

ENTRYPOINT ./existence.sh
