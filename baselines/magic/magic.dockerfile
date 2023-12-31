FROM python:3.8

WORKDIR /home
RUN apt update
RUN apt install git -y
RUN pip install --upgrade pip
RUN git clone https://github.com/IBCNServices/Magic.git

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR Magic/
RUN git clone https://github.com/IBCNServices/INK.git
RUN pip install -e INK/

ADD main.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh
