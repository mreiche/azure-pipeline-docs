# Azure Pipeline docs

Generate documentation from *Azure Pipeline* files.

## Quick start

Build the container
```shell
docker build -t azure-pipeline-docs:latest .
```

And run
```shell
docker run \
-eOUTPUT_DIR="$(pwd)/out" \
-v"$(pwd):$(pwd)" \
azure-pipeline-docs:latest "$(pwd)/test/test-pipeline.yml" 
```
See `out/test-pipeline.md` for details.

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
