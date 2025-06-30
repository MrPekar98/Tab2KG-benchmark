FROM python:3.9.13

RUN apt update
RUN apt install git -y
RUN git clone https://github.com/dylanlty/CitySTI-2024.git

WORKDIR CitySTI-2024/
RUN pip install -r requirements.txt
RUN rm lookup.py
ADD lookup.py .
ADD gemini_main.py .
ADD gemini_candidates.py .
ADD evaluate.sh .
ADD experiments/ .

ENTRYPOINT ./evaluate.sh
