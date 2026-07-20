---
layout: default
title: "Everyday Neuroscience Lab"
---

<section class="hero">
  <p class="eyebrow">Brain Science · Learning · Mental Care</p>
  <h1>뇌과학을 쉽게, 배움과 회복에 쓸 수 있게.</h1>
  <p>Everyday Neuroscience Lab은 매일 쏟아지는 뇌과학 연구 중 부모·교사·학습자에게 실제로 도움이 되는 지식 하나를 골라 쉽게 해석합니다.</p>
  <div class="cta-row">
    <a class="button" href="{{ '/about/' | relative_url }}">블로그 소개</a>
    <a class="button ghost" href="#latest">최신 글 보기</a>
  </div>
  <figure class="hero-visual">
    <img src="{{ '/assets/images/hero/neuroscience-hero.svg' | relative_url }}" alt="뇌과학·학습·회복을 상징하는 일러스트" loading="eager">
  </figure>
</section>

<section class="principles">
  <div><strong>검증</strong><span>논문·학술지·PubMed 근거를 확인합니다.</span></div>
  <div><strong>쉬운 해설</strong><span>전문용어를 생활 언어로 바꿉니다.</span></div>
  <div><strong>교육 적용</strong><span>부모·교사·학습자가 쓸 기준을 남깁니다.</span></div>
  <div><strong>공익성</strong><span>마음과 배움의 정보 격차를 줄입니다.</span></div>
</section>

<section id="latest">
  <h2>최신 글</h2>
  <div class="post-list">
    {% for post in site.posts limit:12 %}
      <article class="post-card">
        {% if post.image %}
        <a class="post-thumb-link" href="{{ post.url | relative_url }}" aria-label="{{ post.title }}">
          <img src="{{ post.image | relative_url }}" alt="{{ post.image_alt | default: post.title }}" loading="lazy">
        </a>
        {% endif %}
        <p class="date">{{ post.date | date: "%Y.%m.%d" }}</p>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        <p>{{ post.description | default: post.excerpt | strip_html | truncate: 140 }}</p>
        <a class="read-more" href="{{ post.url | relative_url }}">읽기 →</a>
      </article>
    {% endfor %}
  </div>
</section>
