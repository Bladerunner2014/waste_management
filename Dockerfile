FROM python:3.11-slim-buster
RUN apt-get update \
    && apt-get install -y --no-install-recommends
RUN pip install --upgrade pip
WORKDIR /infra
# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .


