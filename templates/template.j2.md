# {{ spec.file.name }}

{% if spec.doc.ca.comment %}
{% with comments=spec.doc.ca.comment %}
{% include "comments.j2" %}
{% endwith %}
{% endif %}

{% if spec.doc.stages %}
## Workflow
{% with stages=spec.doc.stages, level = 0 %}
{% include 'stages.j2' %}
{% endwith %}
{% endif %}

{% if spec.doc.jobs %}
## Workflow
{% with jobs=spec.doc.jobs, level=0 %}
{% include 'jobs.j2' %}
{% endwith %}
{% endif %}

## Usage
```yaml
- template: {{ spec.file.name }}@templatesRepository
  parameters: {}  # See below
```

{% if spec.doc.parameters %}
## Parameters
{% include 'parameters.j2' %}
{% endif %}
