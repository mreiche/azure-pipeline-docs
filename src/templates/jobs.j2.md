{%- for job in jobs -%}

{%- if 'Template' in job.__class__.__name__ -%}

{% with jobs=job.spec.doc.jobs, level=level -%}
{% include "jobs.j2.md" %}
{% endwith -%}

{%- else -%}
{{ '    ' * level }}1. *Job*: {{ job.displayName if "displayName" in job else job.job }}
{%- endif -%}

{%- endfor -%}
