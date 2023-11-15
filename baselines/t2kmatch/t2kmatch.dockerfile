FROM tab2kg_benchmark:latest

RUN DEBIAN_FRONTEND=noninteractive apt install git openjdk-11-jdk maven tar -y
RUN git clone https://github.com/olehmberg/T2KMatch.git

WORKDIR T2KMatch/
RUN mvn clean package -DskipTests
RUN mkdir kg/
ADD data/ kg/
RUN mv data/OntologyDBpedia kg/
RUN tar -xf kg/OntologyWikidata.tar.gz
