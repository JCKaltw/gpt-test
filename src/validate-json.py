# src/validate-json.py
import argparse
import json
import sys

import jsonschema  # third-party library for JSON Schema validation
from jsonschema import exceptions as jsonschema_exceptions

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
        # Could be FileNotFoundError or JSONDecodeError (invalid JSON)
        print("ERROR")
        if args.verbose:
            print(f"Failed to load JSON schema: {e}")
        sys.exit(1)

    # Load and parse the JSON data file
    try:
        with open(args.json_file, "r") as json_f:
            data = json.load(json_f)
    except Exception as e:
        # Handle file not found or invalid JSON in the data file
        print("ERROR")
        if args.verbose:
            print(f"Failed to load JSON file: {e}")
        sys.exit(1)

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema_exceptions.ValidationError as e:
        # JSON data is invalid under the schema
        print("ERROR")
        if args.verbose:
            print(f"Validation failed: {e.message}")
        sys.exit(1)
    except jsonschema_exceptions.SchemaError as e:
        # The schema itself is invalid
        print("ERROR")
        if args.verbose:
            print(f"Invalid schema: {e.message}")
        sys.exit(1)

    # If validation succeeds (no exception was raised)
    print("OK")
    sys.exit(0)


# Entry point for script execution
if __name__ == "__main__":
    main()
