FROM tab2kg_benchmark:latest

RUN DEBIAN_FRONTEND=noninteractive

WORKDIR /lexma
ADD lexma.py .
