FROM tiangolo/uwsgi-nginx-flask:flask-index-upload

COPY ./app /app

# custom supervisord config
COPY ./app/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# dev tools (mainly the C Compiler you'll need to uWSGI)
RUN apt-get update && apt-get install -y build-essential

#install miniconda2
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-4.3.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

ENV PATH /opt/conda/bin:$PATH

# Add conda-forge channel
RUN conda config --add channels conda-forge && conda config --add channels bioconda && conda env create -n backend -f environment.yml

# activate the app environment
ENV PATH /opt/conda/envs/backend/bin:$PATH
