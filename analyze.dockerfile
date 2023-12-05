FROM ubuntu:20.04

WORKDIR /home

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install python3 pip openjdk-11-jdk -y
RUN pip3 install neo4j seaborn matplotlib

ENTRYPOINT ./setup/analysis/analyze.sh
