FROM ubuntu:20.04

RUN apt update

WORKDIR /benchmarks
ENTRYPOINT benchmark.sh
