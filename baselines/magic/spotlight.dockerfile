FROM openjdk:8-jre-slim-bullseye

ARG KG

WORKDIR /spotlight
RUN apt update
RUN apt install wget
RUN wget -O spotlight.jar https://sourceforge.net/projects/dbpedia-spotlight/files/latest/download

RUN mkdir ${KG}
ADD ${KG} ${KG}

ENTRYPOINT java -jar spotlight.jar ${KG} http://localhost:2222/rest
