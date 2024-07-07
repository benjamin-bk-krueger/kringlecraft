# World Report {{ world.name }}

[TOC]

## About this Report

This report was created on [KringleCraft](https://www.kringlecraft.com) /ˈkrɪŋ.ɡəl krɑːft ˈkɑːm/. An online CTF solution editor and report generator inspired by [SANS Holiday Hack Challenge](https://www.sans.org/mlp/holiday-hack-challenge/). Makes creating solutions and reports easy and fun 😀

<img src="{{www_server}}{{ url_for('static', filename='img/kringle_logo_t.png') }}" alt="Report Image" style="zoom: 33%;">

## About {{ world.name }}

{{ world.description }}

{%  if world_image %}
<img src="{{www_server}}{{ url_for('static', filename='uploads' + "/" + world_image[0] + "/" + world_image[1]) }}" alt="World Image" style="zoom: 33%;">
{% else %}
<img src="{{www_server}}{{ url_for('static', filename='img/not_found.jpg') }}" alt="World Image" style="zoom: 33%;">
{% endif %}

## About the Author {{ user.name }}

{{ user.description }}

{%  if user_image %}
<img src="{{www_server}}{{ url_for('static', filename='uploads' + "/" + user_image[0] + "/" + user_image[1]) }}" alt="User Image" style="zoom: 33%;">
{% else %}
<img src="{{www_server}}{{ url_for('static', filename='img/not_found.jpg') }}" alt="User Image" style="zoom: 33%;">
{% endif %}

## Report Summary and Notes

{{ md_summary | safe }}

## Content

### Rooms

{% for room in rooms %}
* {{ room.name }}
{% endfor %}

### Objectives

{% for objective in objectives %}{% if objective.difficulty > 0 and objective.visible == 1 %}
* {{ objective.name }}
{% endif %}{% endfor %}

### Hints, Characters and Items

{% for objective in objectives %}{% if objective.difficulty == 0 and objective.visible == 1 %}
* {{ objective.name }}
{% endif %}{% endfor %}
