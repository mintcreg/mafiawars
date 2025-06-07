# pull official base image
FROM python:3.9-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- START OF ADDED SECTION ---
# Install system dependencies needed to build Python packages
# build-essential: provides compilers like gcc
# libpq-dev: headers for connecting to PostgreSQL
# libjpeg-dev/zlib1g-dev: headers for the Pillow image library
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
  # Clean up the apt cache to keep the image small
  && rm -rf /var/lib/apt/lists/*
# --- END OF ADDED SECTION ---

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /usr/src/app/
