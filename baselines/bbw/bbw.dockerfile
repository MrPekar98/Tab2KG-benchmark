FROM tab2kg_benchmark:latest

RUN DEBIAN_FRONTEND=noninteractive apt install python3 python3-pip -y
RUN pip3 install bbw pandas

WORKDIR /bbw
ADD bbwWrapper.py .