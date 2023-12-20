FROM python:3.8

RUN apt update
RUN pip install nltk pandas

WORKDIR /lexma
ADD download_nltk.py .
RUN python download_nltk.py

ADD lexma.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh
