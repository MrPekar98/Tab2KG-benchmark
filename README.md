# Table to KG Entity Linking Benchmark
Table to KG entity linking benchmark evaluation scalability, data dynamism, and KG generality.

## Setup
Before executing the benchmark, the table corpora must be downloaded and processed, Wikidata and DBpedia must be downloaded, and a Neo4J instance must be setup and populated with the two knowledge graphs.
All of this is wrapped in a single Docker file `setup.dockerfile`.
To start setting up the experiments, run the following commands

```bash
docker build -t tab2kg_setup -f setup.dockerfile .
docker run --rm -v ${PWD}/setup:/home -v ${PWD}/benchmarks:/benchmarks tab2kg_setup
```

This will setup the entire benchmark.
Keep in mind this is a very slow process, as there is a lot of data to be processed!

## Running Benchmark
Executing the benchmark is simple.
Similar to setting up the benchmark, run the following commands to start the benchmark

```bash
mkdir -p results
docker build -t tab2kg_benchmark -f evaluate.dockerfile .
docker run --rm -v ${PWD}/setup:/data -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results tab2kg_benchmark
```

All the results are now stored in the `results/` folder.

## Resources Summary
We summarize the corpora used in this benchmark and their golden standard.

- <a href="http://webdatacommons.org/webtables/goldstandardV2.html">WebDataCommons</a>
- <a href="https://sem-tab-challenge.github.io/2023/">SemTab 2023</a>
- <a href="https://zenodo.org/record/7419275">Tough Tables</a>
- <a href="https://zenodo.org/record/4282879">SemTab 2020 Synthetic</a>
- WikiTables from 2019

// TODO: Make description of characteristica of each dataset. Some might contain spelling errors or something else that make them interesting to evaluate entity linkers against.

### Potential Corpora
- <a href="https://opendata.camden.gov.uk/">UKGOV, Camden Council data</a>
- <a href="https://developer.imdb.com/non-commercial-datasets/">IMDB</a>
- <a href="https://gittables.github.io/">GitTables</a>
- <a href="https://webdatacommons.org/webtables/">Web Tables</a>
