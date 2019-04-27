# A linked-data enabled smart client for spotify's api

## Pre-requisites
Kindly install docker, redis and graphviz on the system. Also ensure that you have spotify installed on your system (this doesn't need a premium account).


## Getting Started
In order to get started you'll need to install the dependencies by creating a virtual environment.
Follow the commands given below

```bash
cd SE-Project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

After installing the requirements, you'll have to setup redisgraph server using docker -> 

```bash
docker run -p 6379:6379 -it --rm redislabs/redisgraph
```

Once the server is up, you can run the project in a new terminal instance using the steps below ->

```bash
cd tobie
python querying.py
```

To get information about commands and operations, type help on the prompt.
