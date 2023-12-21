FROM nvidia/cuda:11.1.1-devel-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.9 \
    && apt-get -y install python3-pip \
    && python3 -m pip install -U pip && \
	apt-get install ffmpeg libsm6 libxext6 -y && \ 
    apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y && \
	apt-get install git-all -y && \
	apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install git+https://github.com/facebookresearch/segment-anything.git
RUN pip install -qq -U diffusers==0.11.1 transformers ftfy gradio accelerate
RUN pip install dlib==19.9.0