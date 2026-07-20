# mini-rag 

this is test proj for nhc
## Requirements
- py 3.11 or Later


## just to make sure 
- u can use windows or linux not mac.
## for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### Setup the environment

conda activate mini-rag-app

#### Install Dependencies

```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```
### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### (Optional) Run Ollama Local LLM Server using Colab + Ngrok

- Check the [notebook](https://colab.research.google.com/drive/1KNi3-9KtP-k-93T3wRcmRe37mRmGhL9p?usp=sharing) + [Video](https://youtu.be/-epZ1hAAtrs)

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```
### Setup the environment variables

```bash
$ cp .env.example .env
```
### Run Alembic Migration

```bash

$ alembic upgrade head
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials



```bash
$ cd docker
$ sudo docker compose up -d
```
## Access Services

- **FastAPI**:
- **Flower Dashboard**: 
- **Grafana**:
- **Prometheus**: 
