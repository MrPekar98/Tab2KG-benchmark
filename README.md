# Table to KG Entity Linking Benchmark
Table to KG entity linking benchmark evaluation scalability, data dynamism, and KG generality.

Before setting up this benchmark, make sure you have at least 1.5T disk space available.

## Setup
Before executing the benchmark, the table corpora must be downloaded and processed, Wikidata and DBpedia must be downloaded, and a Neo4J instance must be setup and populated with the two knowledge graphs.
All of this is wrapped in a single Docker file `setup.dockerfile`.
To start setting up the experiments, run the following commands

```bash
docker build -t tab2kg_setup -f setup.dockerfile .
docker run --rm -v ${PWD}/setup:/home -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines:/baselines tab2kg_setup
```

This will setup the entire benchmark.
Keep in mind this is a very slow process, as there is a lot of data to be processed!

## Running Benchmark
Executing the benchmark is simple.
Similar to setting up the benchmark, run the following commands to start the benchmark

```bash
mkdir -p results
docker network create evaluation
docker pull searx/searx
docker run --rm -d -v ${PWD}/searx:/etc/searx --network evaluation -e BASE_URL=http://localhost:3030/ searx/searx
./build-images.sh
docker run --rm --network evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/setup/:/setup -v ${PWD}/results:/results tab2kg_benchmark
```

All the results are now stored in the `results/` folder.

## Resources Summary
We summarize the corpora used in this benchmark and their golden standard.

- <a href="http://webdatacommons.org/webtables/goldstandardV2.html">WebDataCommons</a>
  - Web HTML tables
  - Contains ambiguities
  - Large scale suitable for scalability evaluation (233 million tables)
- <a href="https://zenodo.org/record/7416036">HardTables</a>
  - Noisy, contains spelling errors and ambiguities
- <a href="https://zenodo.org/record/7419275">Tough Tables</a>
  - Complement to SemTab tables
  - Contains more noise
  - Ensures human annotators can resolve ambiguities
- <a href="https://zenodo.org/record/8082116">WikiTables</a>
  - Large corpus of clean Wikipedia tables
  - There is no noise
  - Entity cells are annotated with their corresponding Wikipedia page which can be used to construct ground truth using DBpedia and Wikidata
- <a href="https://zenodo.org/record/7319654">BioDivTab</a>
  - Domain-specific corpus about bio diversity
  - Links to both Wikidata and DBpedia

## Dataset Analysis
Below is listed the average dimensions and number of entities in the datasets used in this repository.
There is also a plot that shows the type distribution of the knowledge graph entities involved in the tabular datasets.
This helps us understand the domains of the table entities.

To run the analysis process, run the following commands.
But first, make sure you set the ownership of the files in setup to yourself.

```bash
sudo chown ${USER} setup/
sudo chown ${USER} setup/**/
```

You can now build the image and start analyzing the datasets.

```bash
docker build -f analyze.dockerfile -t tab2kg_analysis .
docker run --rm -v ${PWD}:/plots -v ${PWD}/benchmarks:/home/benchmarks -v ${PWD}/setup:/home/setup tab2kg_analysis
```

The plots are then saved in `setup/analysis/` as PDF files.

// TODO: Insert plots
