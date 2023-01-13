# Akvo-ResponseGrouper

![PyPI](https://img.shields.io/pypi/v/AkvoResponseGrouper)
[![Build Status](https://github.com/akvo/Akvo-ResponseGrouper/actions/workflows/test.yml/badge.svg)](https://github.com/akvo/Akvo-ResponseGrouper/actions) [![Repo Size](https://img.shields.io/github/repo-size/akvo/Akvo-ResponseGrouper)](https://img.shields.io/github/repo-size/akvo/Akvo-ResponseGrouper) [![Coverage Status](https://coveralls.io/repos/github/akvo/Akvo-ResponseGrouper/badge.svg?branch=main)](https://coveralls.io/github/akvo/Akvo-ResponseGrouper?branch=main) [![Languages](https://img.shields.io/github/languages/count/akvo/Akvo-ResponseGrouper
)](https://img.shields.io/github/languages/count/akvo/Akvo-ResponseGrouper
) [![Issues](https://img.shields.io/github/issues/akvo/Akvo-ResponseGrouper
)](https://img.shields.io/github/issues/akvo/Akvo-ResponseGrouper
) [![Last Commit](https://img.shields.io/github/last-commit/akvo/Akvo-ResponseGrouper/main
)](https://img.shields.io/github/last-commit/akvo/Akvo-ResponseGrouper/main) [![Documentation Status](https://readthedocs.org/projects/Akvo-ResponseGrouper/badge/?version=latest)](https://Akvo-ResponseGrouper.readthedocs.io/en/latest/?badge=latest) [![GitHub license](https://img.shields.io/github/license/akvo/Akvo-ResponseGrouper.svg)](https://github.com/akvo/Akvo-ResponseGrouper/blob/main/LICENSE)

Fast-API Response catalog for pre-computed query

## Install
```
$ pip install AkvoResponseGrouper
```

## Schema Requirements

Please follow [the required schema](https://github.com/akvo/Akvo-ResponseGrouper/blob/main/docs/database.org) before using AkvoResponseGrouper.

## Usage

1. Database Migration

Database migration is the first required step for AkvoResponseGrouper to work. Use the akvo-responsegrouper CLI to migrate all data sources with JSON configuration files to generate Materialized Views that AkvoResponseGrouper can then use.

```bash
$ akvo-responsegrouper
usage: akvo-responsegrouper [-h] [-c CONFIG] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        akvo-responsegrouper -c <json_file_config>
  -d, --drop            Drop the ar_category view table
```

2. Router

To get the new endpoint provided by AkvoResponseGrouper, import the collection route to the App by:

```python
from fastapi import FastAPI
from AkvoResponseGrouper.routes import collection_route

app = FastAPI(
    root_path="/",
    title="Akvo Response Grouper Demo",
)

app.include_router(collection_route)

@app.get("/", tags=["Dev"])
def read_main():
    return "OK"
```

3. Query



## Development

### Run Dev Containers

The dev environment contains two containers: FastAPI backend and PostGres db, to run:

```bash
docker compose up -d
```
Before go to the next step, wait until the service started at [http://localhost:5000](http://localhost:5000).

### Seed Necessary Data

In order to debug the data itself. We need to seed the example form and fake datapoints

###
```bash
docker compose exec backend python -m script.seeder_form
docker compose exec backend python -m script.seeder_datapoint <number_of_datapoint>
```

### Migration

Dev environment uses contents that is available in `Akvo-ResponseGrouper/src/AkvoResponseGrouper`. To create the Category Materialized View via CLI in dev environment:

Upgrade:

```bash
python -m AkvoResponseGrouper.cli.migrate -c './sources/category.json'
```

After upgrade, you can see "AkvoResponseGrouper - Collection" is available in API docs, ussualy [http://locahhost:5000/docs](http://localhost:5000/docs) (Depends on the root path api).

Downgrade:
```
python -m AkvoResponseGrouper.cli.migrate -c './sources/category.json'
```

### Teardown
```
docker compose down -v
```
