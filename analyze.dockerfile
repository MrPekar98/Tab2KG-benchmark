FROM ubuntu:20.04

WORKDIR /home

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install python3 pip openjdk-11-jdk -y
RUN pip3 install neo4j

ENTRYPOINT ./setup/analysis/analyze.sh
