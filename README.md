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
  - Web HTML tables
  - Contains ambiguities
  - Large scale suitable for scalability evaluation (233 million tables)
- <a href="https://sem-tab-challenge.github.io/2023/">SemTab 2023</a>
  - Noisy, contains spelling errors and ambiguities
- <a href="https://zenodo.org/record/7419275">Tough Tables</a>
  - Complement to SemTab tables
  - Contains more noise
  - Ensures human annotators can resolve ambiguities
- <a href="https://zenodo.org/record/8082116">WikiTables</a>
  - Large corpus of clean Wikipedia tables
  - There is no noise
  - Entity cells are annotated with their corresponding Wikipedia page which can be used to construct ground truth using DBpedia and Wikidata
