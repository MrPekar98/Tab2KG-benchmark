FROM ubuntu:20.04

WORKDIR /home

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install python3 pip wget openjdk-11-jdk bzip2 zip git -y
RUN pip3 install neo4j

ENTRYPOINT ./setup.sh