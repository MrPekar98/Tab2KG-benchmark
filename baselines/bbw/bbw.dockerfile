FROM ubuntu:20.04

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install python3 python3-pip git -y
RUN pip3 install bbw pandas

WORKDIR /bbw
ADD bbwWrapper.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh
