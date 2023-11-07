FROM tab2kg_benchmark:latest

RUN DEBIAN_FRONTEND=noninteractive openjdk-17-jdk maven git -y
RUN git clone https://github.com/MrPekar98/keyword-kg-linker.git
WORKDIR keyword-kg-linker/
