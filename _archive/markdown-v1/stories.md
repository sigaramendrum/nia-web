---
layout: page
title: "Stories"
permalink: /stories/
---

<section class="band blush" markdown="1">

# Stories

Take a limitation and turn it into an opportunity. Take an opportunity and turn it into an adventure. Dream big!

</section>

<section class="band white">
<ul class="cards">
{% for post in site.posts %}
  <li>
    <a href="{{ post.url | remove_first: '/' }}"><img src="{{ post.image }}" alt="" loading="lazy"><strong>{{ post.title }}</strong></a>
  </li>
{% endfor %}
</ul>
</section>
