#this is Debian based, specifically Debian8.5
FROM continuumio/miniconda3:4.3.11

ADD . /app
WORKDIR /app

# dev tools (mainly the C Compiler you'll need to uWSGI)
RUN sudo get update && apt-get install build-essential

# Add conda-forge channel
RUN conda config --add channels conda-forge && conda config --add channels bioconda && conda env create -n backend -f environment.yml

# activate the app environment
ENV PATH /opt/conda/envs/backend/bin:$PATH
