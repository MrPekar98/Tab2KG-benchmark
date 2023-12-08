FROM python:3.8

ARG KG

WORKDIR /home
RUN apt update
RUN apt install git -y
RUN git clone https://github.com/IBCNServices/Magic.git

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR Magic/
RUN git clone https://github.com/IBCNServices/INK.git
RUN pip install -e INK/

ADD dbpedia-10-2016/ dbpedia-10-2016/
ADD dbpedia-03-2022/ dbpedia-03-2022/
ADD ${KG}.hdt .
ADD main.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh ${KG}
