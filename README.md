# Akvo-ResponseGrouper
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

2. HTTP Router

Soon...

## Development

```bash
cd dev
docker compose up -d
```
Wait until migration process is done

```bash
docker compose exec backend python -m script.seeder_form
docker compose exec backend python -m script.seeder_datapoint <number_of_datapoint>
```
