#!/bin/sh
. ./source-venv.sh

echo "python src/validate-json.py --verbose \ "
echo "    --json-schema-file schemas/ddl-ast-schema.json \ "
echo "    data/ddl-ast.json "

python src/validate-json.py --verbose \
    --json-schema-file schemas/ddl-ast-schema.json \
    data/ddl-ast.json
