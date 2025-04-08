# {{ spec.file.name }}

{% if spec.doc.stages %}
## Workflow
{% include 'pipeline.j2.md' %}
{% endif %}

## Example
```yaml
- template: build-docker-template.yml@templatesRepository
  parameters:
    hasHelm: true  # Repository also contains a helm chart
    chartPath: "./helm"  # Chart base path relative to your repository
    imageTagUpdatePath: '.image.tag'  # Structure path to your image tag reference in values.yml
    useSemanticVersion: true  # Force usage of semantic versioning
    chartName: $(Build.Repository.Name)  # The name of the chart, MUST match the chart name of Chart.yml
    repository: $(Build.Repository.Name)  # The chart's repository name in the registry
    dockerFile: "Dockerfile"  # Optional: Path to the container file
```

{% if spec.doc.parameters %}
## Parameters
{% include 'parameters.j2.md' %}
{% endif %}
