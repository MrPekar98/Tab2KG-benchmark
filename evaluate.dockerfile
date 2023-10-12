FROM ubuntu:20.04

WORKDIR /home

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install python3 pip wget gzip git openjdk-11-jdk mvn -y

# EmbLookup
RUN git clone https://github.com/MrPekar98/EmbLookup.git
WORKDIR EmbLookup/
RUN pip3 install -r requirements.txt
RUN ./setup.sh

WORKDIR /home

# TK2Match
RUN git clone https://github.com/olehmberg/T2KMatch.git
WORKDIR T2KMatch/
RUN mvn clean package -DskipTests
ADD baselines/tk2match.sh .

# bbw
WORKDIR /home
RUN pip install pandas bbw
RUN mkdir bbw/
WORKDIR bbw/
ADD baselines/bbwWrapper.py .
