| Name | Type | Default |
|------|------|---------|
{% for param in spec.doc.parameters -%}
| {{ param.name }} | {{ param.type }} | {% if param.default %}`{{ param.default }}`{% endif %} |
{% endfor %}
