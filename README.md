# Azure Pipeline Docs

Generate documentation from *Azure Pipeline* files.

## Quick start

Build the container
```shell
docker build -t azure-pipeline-docs:latest .
```

And run
```shell
docker run -d \
-p8198:8198 \
-eOUTPUT_DIR="$(pwd)/out" \
-v"$(pwd):$(pwd)" \
azure-pipeline-docs:latest "$(pwd)/*.yml" 
```

## Usage

### Environment variables
```shell
TEMPLATE_FILE=""  # Optional: Path to the Jinja template file to use for rendering
```

## Templating

See the [templates folders](templates), how to render the documentation. 

## Development and testing

Install the test requirements first:
```shell
pip install -r test-requirements.txt
```
Run the tests
```shell
PYTHONPATH="." pytest test
```
