FROM tab2kg_benchmark:latest

RUN DEBIAN_FRONTEND=noninteractive apt install python3 python3-pip wget gzip git -y
RUN git clone https://github.com/MrPekar98/EmbLookup.git

WORKDIR EmbLookup/
RUN mkdir aliases/
ADD aliases/ aliases/

RUN python3 -m pip install -r requirements.txt
RUN wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz
RUN gzip -d cc.en.300.bin.gz
RUN mkdir -p embeddings/
RUN mv cc.en.300.bin embeddings/
