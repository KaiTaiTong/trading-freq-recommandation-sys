FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    sqlite3 \
    gfortran \
    libbz2-dev \
    libsqlite3-dev \
    libtiff-dev \
    libcurl4-openssl-dev \
    libpq-dev \
    libpcre2-dev \
    libgeos-dev \
    libhdf4-dev \
    pkg-config \
    cmake \
    r-base \
    r-cran-randomforest \
    xvfb \
    xauth \
    xfonts-base \
    python3.7 \
    python3.7-distutils \
    python3.7-dev \
    default-jre-headless

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN update-alternatives --set python /usr/bin/python3.7

RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py --force-reinstall && \
    rm get-pip.py


WORKDIR /trading-freq-recommandation-sys/
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
