# {{ spec.file.name }}

{% include "custom.j2" %}

{% if spec.doc.stages %}
## Workflow
{% with stages=spec.doc.stages, level = 0 %}
{% include 'stages.j2' %}
{% endwith %}
{% endif %}
