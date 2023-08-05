FROM ubuntu:latest
MAINTAINER Colin Bitterfield <cbitterfield@gmail.com>
USER root

LABEL Description="Production Container for creating preview Images and Database."
LABEL License="GNU Public License 3.0"
LABEL Usage="docker run -d  -v [database volume]:/data  cbitterfield/mkpreview"
LABEL Version="1.0"
LABEL maintainer="Colin Bitterfield <colin@bitterfield.com>"
LABEL Author="Colin Bitterfield <colin@bitterfield.com>"

ARG DATE_TIMEZONE=UTC
ARG DEBIAN_FRONTEND=noninteractive

# Set up environment
RUN apt-get update && apt-get install -y \
	python \
	python-dev \
	python-pip \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Update the operating system when we start and again at the end.
RUN apt-get update
RUN apt-get upgrade -y

# Add Basic Utilities needed
RUN apt-get install -y zip unzip
RUN apt install debconf-utils sudo -y
RUN apt-get install git nano tree vim curl ftp ssh  -y
RUN apt-get install libmagickwand-dev imagemagick ffmpeg -y

# Add python3
RUN apt-get install python3 python3-pip -y
RUN echo  "alias python='python3'" >> ~/.bashrc
RUN echo  "alias pip='pip3'" >> ~/.bashrc

RUN mkdir /data
RUN mkdir /videos

# TODO: update this libraries
RUN pip3 install wheel==0.32.1 \
	watchdog==0.9.0 \
	pillow==6.2.1 \
    wand==0.5.7 \
    ffmpeg-python==0.2.0 \
    twine==1.13.0


RUN pip3 install mkpreview


WORKDIR /mkpreview
VOLUME /data

ENTRYPOINT ["/bin/bash"]
