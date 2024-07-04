FROM python:3.8

RUN pip install pandas requests beautifulsoup4 ftfy langid
WORKDIR /bbw

ADD bbw.py .
ADD main.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh
