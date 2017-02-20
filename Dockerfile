FROM continuumio/miniconda3:latest

ADD . /app
WORKDIR /app

# Add conda-forge channel
RUN conda config --add channels conda-forge && conda config --add channels bioconda && conda env create -n backend -f environment.yml

# activate the app environment
ENV PATH /opt/conda/envs/backend/bin:$PATH
