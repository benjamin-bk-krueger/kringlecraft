# Objective Report: {{ objective.name }}

## {{ objective_types[objective.type] }} {{ objective.name }} Report

### Objective Details

{% if objective_image %}
![{{ objective_types[objective.objective_type] }} Image]({{www_server}}{{ url_for('static', filename='uploads/' + objective_image[0] + "/" + objective_image[1]) }})
{% else %}
![Objective Image]({{www_server}}{{ url_for('static', filename='img/not_found.jpg') }})
{% endif %}

**Name:** {{ objective.name }}

{% if objective.difficulty > 0 %}
**Difficulty:** {% for i in range(objective.difficulty) %}🌳{% endfor %}
{% endif %}

**Description:** {{ objective.description }}

### Challenge

{{ md_challenge | striptags }}

### Solution

{{ md_solution | striptags }}
