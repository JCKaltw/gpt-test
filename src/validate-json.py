# src/validate-json.py
import argparse
import json
import sys
import os

import jsonschema
from jsonschema import Draft7Validator, RefResolver, exceptions as jsonschema_exceptions

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

    # If your schema (e.g., dml-ast-schema.json) contains external references,
    # you can load the referenced schemas into a "store" mapping.
    # For example, if dml-ast-schema.json references ddl-ast-schema.json via:
    #   "$ref": "https://pgpro.plasmaguardllc.com/ddl-ast-schema.json/#definitions/table"
    # then load ddl-ast-schema.json and map its $id to its contents.
    store = {}
    # Check if our schema has external references that need to be resolved.
    # Here we assume that if you’re validating the DML schema, you'll need the DDL schema.
    # Adjust the path as needed.
    ddl_schema_path = os.path.join(os.path.dirname(args.json_schema_file), "ddl-ast-schema.json")
    try:
        with open(ddl_schema_path, "r") as ddl_f:
            ddl_schema = json.load(ddl_f)
            # Map the remote URI to the loaded ddl_schema
            store["https://pgpro.plasmaguardllc.com/ddl-ast-schema.json"] = ddl_schema
    except Exception:
        # If the ddl schema is not needed or cannot be loaded, skip it.
        pass

    # Create a resolver with the custom store.
    resolver = RefResolver.from_schema(schema, store=store)

    # Validate using a Draft7Validator with the custom resolver
    try:
        validator = Draft7Validator(schema, resolver=resolver)
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
