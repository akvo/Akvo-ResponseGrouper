#!/usr/bin/env bash

set -euo pipefail

pip install -r ./requirements.txt

uvicorn main:app --reload
