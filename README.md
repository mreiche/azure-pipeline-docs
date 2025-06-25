[![Tests Status](https://github.com/mreiche/azure-pipeline-docs/actions/workflows/test-and-build.yml/badge.svg)](https://github.com/mreiche/owasp-dependency-track-cli/actions/workflows/test-and-build.yml)

# Azure Pipeline docs

Generate documentation from *Azure Pipeline* files.

## Quick start
```shell
docker run \
-eOUTPUT_DIR="$(pwd)/out" \
-v"$(pwd):$(pwd)" \
ghcr.io/mreiche/azure-pipeline-docs:main "$(pwd)/test/test-pipeline.yml" 
```
See `out/test-pipeline.md` for details.

## Usage

### Environment variables
```shell
TEMPLATE_FILE=""  # Optional: Path to the Jinja template file to use for rendering (defaults to `templates/template.j2.md`)
TEMPLATES_DIR=""  # Optional: Additional path for template overrides
OUTPUT_DIR="out"  # Optional: Output directory for the rendering files
SPEC_ROOT=""      # Optional: Path to the root directory of the input files (provides 'spec.relative_path' in templates and keeps the directory structure of output files)
VALIDATE="true"   # Optional: Performs some validation checks on the templates
```

### Templating

The templates are rendered via *Jinja2* and the output files are using the same file extension of the given template file.

The search paths for templates are:
- `TEMPLATES_DIR` if defined
- `SPEC_ROOT` if defined
- Parent directory of `TEMPLATE_FILE`
- Distributed `templates/` directory

You can use this search order to override snippets. See the [templates folders](templates) for examples.

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

## References
- https://docs.docker.com/build/ci/github-actions/multi-platform/
