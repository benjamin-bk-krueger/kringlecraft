# {{ objective_types[objective.type] }} {{ objective.name }} Report

{% if objective_image %}
<img src="{{www_server}}{{ url_for('static', filename='uploads' + "/" + objective_image[0] + "/" + objective_image[1]) }}" alt="{{ objective_types[objective.objective_type] }} Image" style="zoom: 33%;">
{% else %}
<img src="{{www_server}}{{ url_for('static', filename='img/not_found.jpg') }}" alt="Objective Image" style="zoom: 33%;">
{% endif %}  

### Description
{{ objective.description }}  
**Difficulty**: ({{ objective.difficulty }})   

### Challenge
{{ md_challenge | safe }}  

### Solution
{{ md_solution | safe }}  
