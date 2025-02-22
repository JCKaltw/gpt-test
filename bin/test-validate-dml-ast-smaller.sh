#!/bin/sh
. ./source-venv.sh

echo "python src/validate-json.py --verbose \ "
echo "    --json-schema-file schemas/dml-ast-schema.json \ "
echo "    data/dml-ast-smaller.json "

python src/validate-json.py --verbose \
    --json-schema-file schemas/dml-ast-schema.json \
    data/dml-ast-smaller.json
