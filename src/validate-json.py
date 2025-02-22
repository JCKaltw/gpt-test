# src/validate-json.py
import argparse
import json
import sys
import os

import jsonschema
from jsonschema import Draft7Validator, exceptions as jsonschema_exceptions
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Validate a JSON file against a JSON schema.")
    parser.add_argument("--json-schema-file", dest="json_schema_file", required=True,
                        help="Path to the JSON schema file")
    parser.add_argument("json_file", help="Path to the JSON data file to validate")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Display detailed error messages if validation fails")
    args = parser.parse_args()

    # Load and parse the JSON schema file
    try:
        with open(args.json_schema_file, "r") as schema_f:
            schema = json.load(schema_f)
    except Exception as e:
        print("ERROR")
        if args.verbose:
            print(f"Failed to load JSON schema: {e}")
        sys.exit(1)

    # Load and parse the JSON data file
    try:
        with open(args.json_file, "r") as json_f:
            data = json.load(json_f)
    except Exception as e:
        print("ERROR")
        if args.verbose:
            print(f"Failed to load JSON file: {e}")
        sys.exit(1)

    # Create a registry to store referenced schemas
    registry = Registry()

    # Load the referenced schema (ddl-ast-schema.json) and add it to the registry
    ddl_schema_path = os.path.join(os.path.dirname(args.json_schema_file), "ddl-ast-schema.json")
    try:
        with open(ddl_schema_path, "r") as ddl_f:
            ddl_schema = json.load(ddl_f)
            # Add the referenced schema to the registry using its $id
            registry = registry.with_resource(
                uri="https://pgpro.plasmaguardllc.com/ddl-ast-schema.json",
                resource=Resource.from_contents(ddl_schema, default_specification=DRAFT7),
            )
    except Exception as e:
        print("ERROR")
        if args.verbose:
            print(f"Failed to load referenced schema: {e}")
        sys.exit(1)

    # Validate using a Draft7Validator with the custom registry
    try:
        validator = Draft7Validator(schema, registry=registry)
        validator.validate(data)
    except jsonschema_exceptions.ValidationError as e:
        print("ERROR")
        if args.verbose:
            print(f"Validation failed: {e.message}")
        sys.exit(1)
    except jsonschema_exceptions.SchemaError as e:
        print("ERROR")
        if args.verbose:
            print(f"Invalid schema: {e.message}")
        sys.exit(1)

    # If validation succeeds (no exception was raised)
    print("OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
