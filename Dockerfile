FROM continuumio/miniconda3

RUN apt update && apt install build-essential -y
COPY environment.yml environment.yml
RUN conda env create -f environment.yml
RUN echo 'conda activate diff_pd' >> ~/.bashrc
RUN apt update && apt install cmake -y
RUN apt update && apt install -y --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
    imagemagick-6.q16 \
    libmagickcore-6.q16-6-extra \
    ffmpeg
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
