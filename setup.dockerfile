FROM ubuntu:20.04

WORKDIR /home

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install python3 pip wget openjdk-11-jdk bzip2 curl zip git npm -y
RUN pip3 install neo4j torch pytorch_metric_learning numpy sqlalchemy fasttext pandas
RUN npm install -g ttl-merge

ADD settings.sh /settings

ENTRYPOINT ./setup.sh
