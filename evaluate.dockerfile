FROM ubuntu:20.04

WORKDIR /home

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install python3 pip wget gzip git openjdk-11-jdk openjdk-17-jdk mvn tar -y

RUN mkdir baselines/
ADD baselines/ baselines/

# keyword-kg-linker
RUN git clone https://github.com/MrPekar98/keyword-kg-linker.git

# EmbLookup
RUN git clone https://github.com/MrPekar98/EmbLookup.git
WORKDIR EmbLookup/
RUN pip3 install -r requirements.txt
RUN ./setup.sh

# TK2Match
RUN git clone https://github.com/olehmberg/T2KMatch.git
WORKDIR T2KMatch/
RUN mvn clean package -DskipTests
RUN mkdir new_data
RUN mv /home/baselines/t2kmatch/data/* new_data/
WORKDIR new_data
RUN tar -xf OntologyWikidata.tar.gz

# bbw
WORKDIR /home/baselines/bbw/
RUN pip3 install bbw pandas

# LexMa

# REL

WORKDIR /home
ENTRYPOINT 
