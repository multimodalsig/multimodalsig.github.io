---
layout: page
title: Projects
permalink: /research/projects/
description: Current and recent research projects in the Multimodal Spatial Imaging Lab.
nav: false
---

<div class="projects">
  {% assign sorted_projects = site.projects | sort: "importance" %}
  <div class="row row-cols-1 row-cols-md-2 g-3">
    {% for project in sorted_projects %}
      <div class="col">
        <div class="project-card-expandable" onclick="this.classList.toggle('expanded')">
          <div class="card h-100 hoverable" style="position: relative;">
            <span class="card-expand-icon"><i class="fa-solid fa-chevron-down"></i></span>
            {% if project.img %}
              {% include figure.liquid loading="eager" path=project.img sizes="250px" alt="project thumbnail" class="card-img-top" %}
            {% endif %}
            <div class="card-body">
              <h2 class="card-title">{{ project.title }}</h2>
              <p class="card-text">{{ project.description }}</p>
            </div>
            <div class="card-detail">
              <div class="card-detail-inner">
                {{ project.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
</div>
