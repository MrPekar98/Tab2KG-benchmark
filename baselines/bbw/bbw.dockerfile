FROM python:3.8

RUN apt update
RUN apt install git -y
RUN pip install bbw pandas

WORKDIR /bbw
ADD bbwWrapper.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh
