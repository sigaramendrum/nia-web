---
layout: page
title: "Stories"
permalink: /stories/
---

# Stories

Take a limitation and turn it into an opportunity. Take an opportunity and turn it into an adventure. Dream big!

<ul class="stories">
{% for post in site.posts %}
  <li>
    <a href="{{ post.url }}"><img src="{{ post.image }}" alt="{{ post.title }}" loading="lazy"></a>
    <a href="{{ post.url }}"><strong>{{ post.title }}</strong></a>
  </li>
{% endfor %}
</ul>
