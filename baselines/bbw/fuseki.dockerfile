FROM ubuntu:20.04

WORKDIR /home

RUN apt update
RUN apt install openjdk-17-jdk wget -y
RUN wget https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-server/4.10.0/jena-fuseki-server-4.10.0.jar

EXPOSE 8884
ENTRYPOINT java -jar jena-fuseki-server-4.10.0.jar --loc /tdb --port 8884 /wikidata
