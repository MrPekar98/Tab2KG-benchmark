FROM tab2kg_benchmark:latest

RUN DEBIAN_FRONTEND=noninteractive apt install python3 pip -y
RUN pip3 install nltk pandas

WORKDIR /lexma
ADD lexma.py .
ADD download_nltk.py .
RUN python3 download_nltk