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
TEMPLATE_FILE="templates/template.j2.md"  # Optional: Path to the Jinja template file to use for rendering
OUTPUT_DIR="out"                          # Optional: Output directory for the documentation files
```

### Templating

See the [templates folders](templates) for examples.

## Development and testing

Install the test requirements first:
```shell
pip install -r test-requirements.txt
```
Run the tests
```shell
PYTHONPATH="." pytest test
```

## Alternatives
- Generate Markdown from Azure Pipelines via *mkdocs*: https://github.com/Wesztman/mkdocs-azure-pipelines
