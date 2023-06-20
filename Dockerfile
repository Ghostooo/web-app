#FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
FROM python:3.11
WORKDIR /app/py_image_classification

ADD . .

RUN mkdir /data_ia

ENV http_proxy="http://firewall.ina.fr:81" https_proxy="http://firewall.ina.fr:81"

RUN apt-get --allow-releaseinfo-change -y update && \
    apt-get -y install cmake \
                       libglib2.0-dev \
                       libgl1-mesa-glx \
                       libsm6 \
                       libxrender1 \
                       vim \
                       libsndfile1 \
                       software-properties-common && \
    pip install --upgrade pip

RUN pip install -r requirements.txt

