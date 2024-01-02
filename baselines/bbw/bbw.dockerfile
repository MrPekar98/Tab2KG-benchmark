FROM python:3.8

RUN apt update
RUN apt install git -y
RUN pip install pandas

WORKDIR /bbw
ADD bbwWrapper.py .
ADD bbw.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh
