# World Report: {{ world.name }}

## About this Report

This report was created on [KringleCraft](https://craft.kringle.info), */ˈkrɪŋ.ɡəl krɑːft/*. An online CTF solution editor and report generator inspired by [SANS Holiday Hack Challenge & KringleCon](https://www.sans.org/mlp/holiday-hack-challenge/).

Makes creating solutions and reports easy and fun 😀

![Report Image]({{www_server}}{{ url_for('static', filename='img/kringle_logo_t.png') }})

## About {{ world.name }}

{% if world_image %}
![World Image]({{www_server}}{{ url_for('static', filename='uploads' + "/" + world_image[0] + "/" + world_image[1]) }})
{% else %}
![World Image]({{www_server}}{{ url_for('static', filename='img/not_found.jpg') }})
{% endif %}

{{ world.description }}

## About the Author {{ user.name }}

{{ user.description }}

{% if user_image %}
![User Image]({{www_server}}{{ url_for('static', filename='uploads' + "/" + user_image[0] + "/" + user_image[1]) }})
{% else %}
![User Image]({{www_server}}{{ url_for('static', filename='img/not_found.jpg') }})
{% endif %}

## Report Summary and Notes

{{ md_summary | striptags }}

## Table of Contents

### Rooms
{% for room in rooms %}
- [{{ room.name }}](#Room: {{ room.name | replace(" ", "-") }})
{% endfor %}

### Objectives
{% for objective in objectives %}{% if objective.difficulty > 0 and objective.visible == 1 %}
- [{{ objective.name }}](#Objective: {{ objective.name | replace(" ", "-") }})
{% endif %}{% endfor %}

### Hints, Characters and Items
{% for objective in objectives %}{% if objective.difficulty == 0 and objective.visible == 1 %}
- [{{ objective.name }}](#Hint/Character/Item: {{ objective.name | replace(" ", "-") }})
{% endif %}{% endfor %}

---

{% for room in rooms %}
## Room: {{ room.name | replace(" ", "-") }}

{% if room_images[room.id] %}
![{{ room.name }}]({{www_server}}{{ url_for('static', filename='uploads' + "/" + room_images[room.id][0] + "/" + room_images[room.id][1]) }})
{% else %}
![{{ room.name }}]({{www_server}}{{ url_for('static', filename='img/not_found.jpg') }})
{% endif %}

{{ room.description }}

### Objectives in this room:
{% for objective in objectives %}{% if objective.room_id == room.id %}
- {% if objective.visible == 1 %}[{{ objective.name }}](#Objective: {{ objective.name | replace(" ", "-") }}){% else %}{{ objective.name }}{% endif %}
{% endif %}{% endfor %}

[Back to Rooms List](#rooms)

---

{% endfor %}

{% for objective in objectives %}{% if objective.difficulty > 0 and objective.visible == 1 %}
## Objective: {{ objective.name | replace(" ", "-") }}

**Type:** {{ objective_types[objective.objective_type] }}

{% if objective_images[objective.id] %}
![{{ objective.name }}]({{www_server}}{{ url_for('static', filename='uploads' + "/" + objective_images[objective.id][0] + "/" + objective_images[objective.id][1]) }})
{% else %}
![{{ objective.name }}]({{www_server}}{{ url_for('static', filename='img/not_found.jpg') }})
{% endif %}

{{ objective.description }}

{% if objective.difficulty > 0 %}
**Difficulty:** {% for i in range(objective.difficulty) %}🌳{% endfor %}
{% endif %}

**Room:** {% for room in rooms %}{% if objective.room_id == room.id %}[{{ room.name }}](#Room: {{ room.name | replace(" ", "-") }}){% endif %}{% endfor %}

### Challenge

{% if md_challenges[objective.id] | length < 5 %}
This objective has no challenge yet
{% else %}
{{ md_challenges[objective.id] | striptags }}
{% endif %}

### Solution

{% if md_solutions[objective.id] | length < 5 %}
This objective has no solution yet
{% else %}
{{ md_solutions[objective.id] | striptags }}
{% endif %}

[Back to Objectives List](#objectives)

---

{% endif %}{% endfor %}

{% for objective in objectives %}{% if objective.difficulty == 0 and objective.visible == 1 %}
## Hint/Character/Item: {{ objective.name | replace(" ", "-") }}

**Type:** {{ objective_types[objective.objective_type] }}

{% if objective_images[objective.id] %}
![{{ objective.name }}]({{www_server}}{{ url_for('static', filename='uploads' + "/" + objective_images[objective.id][0] + "/" + objective_images[objective.id][1]) }})
{% else %}
![{{ objective.name }}]({{www_server}}{{ url_for('static', filename='img/not_found.jpg') }})
{% endif %}

{{ objective.description }}

**Room:** {% for room in rooms %}{% if objective.room_id == room.id %}[{{ room.name }}](#Room: {{ room.name | replace(" ", "-") }}){% endif %}{% endfor %}

{% if md_challenges[objective.id] | length > 5 %}
### Challenge

{{ md_challenges[objective.id] | striptags }}
{% endif %}

{% if md_solutions[objective.id] | length > 5 %}
### Solution

{{ md_solutions[objective.id] | striptags }}
{% endif %}

[Back to Hints, Characters and Items List](#hints-characters-and-items)

---

{% endif %}{% endfor %}
