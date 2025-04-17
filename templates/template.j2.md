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
## Jobs
{% with jobs=spec.doc.jobs, level=0 %}
{% include 'jobs.j2' %}
{% endwith %}
{% endif %}

{% if spec.doc.steps %}
## Steps
{% with steps=spec.doc.steps, level=0 %}
{% include 'steps.j2' %}
{% endwith %}
{% endif %}

{% include 'usage.j2' %}


{% if spec.doc.parameters %}
## Parameters
{% include 'parameters.j2' %}
{% endif %}
