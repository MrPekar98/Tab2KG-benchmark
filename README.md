# Table to KG Entity Linking Benchmark
Table to KG entity linking benchmark evaluation scalability, data dynamism, and KG generality.

Before setting up this benchmark, make sure you have at least 1.5T disk space available.

## Setup
Before executing the benchmark, the table corpora must be downloaded and processed, Wikidata and DBpedia must be downloaded, and a Neo4J instance must be setup and populated with the two knowledge graphs.
All of this is wrapped in a single Docker file `setup.dockerfile`.
To start setting up the experiments, run the following commands.

```bash
docker build -t tab2kg_setup -f setup.dockerfile .
docker run --rm -v ${PWD}/setup:/home -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/baselines:/baselines tab2kg_setup
```

This will setup the entire benchmark.
Keep in mind this is a very slow process, as there is a lot of data to be processed!

Enter the directory `setup/existence/`, build the Docker image and run a container to perform existence checking of ground truth entities in KG files, the Virtuoso instance, and the keyword lookup service by running the following set of commands.

```bash
docker build -t existence .
docker network inspect kg-lookup-network >/dev/null 2>&1 || docker network create kg-lookup-network
docker run --rm --name vos_existence -d \
           --network kg-lookup-network \
           -v ${PWD}/../../kg-lookup/database:/database \
           -v ${PWD}/../../kg-lookup/import:/import \
           -t -p 1111:1111 -p 8890:8890 -i openlink/virtuoso-opensource-7:7
docker run --rm --network kg-lookup-network -v ${PWD}:/home \
                -v ${PWD}/../../benchmarks/:/benchmarks \
                -v ${PWD}/../tough_tables/dbpedia/:/dbpedia_16 \
                -v ${PWD}/../kg/dbpedia/:/dbpedia_22 \
                -v ${PWD}/../tough_tables/wikidata/:/wikidata \
                --name existence_checking existence
```

The container will also remove ground truth entities that do not exist in the KG files.

## Running Benchmark
Executing the benchmark is simple.
Similar to setting up the benchmark, run the following commands to start the entire benchmark pipeline.

```bash
./setup-baselines.sh
./benchmark.sh
```

All the results are now stored in the `results/` folder.

To clean up all docker images, container, networks, etc., run the `cleanup.sh` script.

### Evaluating the Results
To evaluate the results, run the following command:

```bash
docker run --rm -v ${PWD}/results/:/results -v ${PWD}/benchmarks/:/benchmarks -v ${PWD}/measure/:/measure python:3.8 python /measure/measure.py
```

This will generate CSV files for different measurement metrics, including precision, recall, F1-score, and runtime.
These CSV can then be used to generate plots.

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
- <a href="https://zenodo.org/records/10048187">tFood</a>
  - Domain-specific corpus about food
  - Links to Wikidata

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
docker run --rm -v ${PWD}/plots/:/plots -v ${PWD}/benchmarks:/home/benchmarks -v ${PWD}/setup:/home/setup tab2kg_analysis
```

The plots are then saved in `plots/` as PDF files.

You can check for ground truth existence by running `./existence.sh` in the `setup/` directory.
This script will check how many of the ground truth entities in each dataset exist in the KG dumps, Virtuoso instance, and Lucene indexes in the KG lookup service.

### Dataset Type Distributions
Below are plots of type distributions of the entities within the datasets used in this benchmark.

#### SemTab HardTables
![Wikidata](./plots/SemTab.pdf)

#### SemTab BioDivTab
![DBpedia](./plots/SemTab_BioDivTab_DBpedia.pdf)

#### SemTab tFood - Table as entity
![Wikidata](./plots/SemTab_tFood_entity_Wikidata.pdf)

#### SemTab tFood - Row as entity
![Wikidata](./plots/SemTab_tFood_horizontal_Wikidata.pdf)

#### Tough Tables
![DBpedia](./plots/ToughTables-DBpedia.pdf)

#### Tough Tables
![Wikidata](./plots/ToughTables-Wikidata.pdf)

#### WebDataCommons
![DBpedia](./plots/WebDataCommons.pdf)

#### WikiTables 2013
![DBpedia](./plots/Wikitables-DBpedia_2013.pdf)
![Wikidata](./plots/Wikitables-Wikidata_2013.pdf)

#### WikiTables 2019
![DBpedia](./plots/Wikitables-DBpedia_2019.pdf)
![Wikidata](./plots/Wikitables-Wikidata_2019.pdf)
