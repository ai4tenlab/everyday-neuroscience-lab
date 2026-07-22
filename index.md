---
layout: default
title: "뉴로시민 | Everyday Neuroscience Lab"
---

<section class="hero">
  <p class="eyebrow">NEUROSCIENCE LITERACY · LEARNING · MIND</p>
  <h1>뇌를 알면, 일상이 보입니다.</h1>
  <p><strong>뉴로시민</strong>은 배움·감정·습관·관계가 우리 뇌에서 어떻게 만들어지고 달라지는지, 연구 근거를 바탕으로 시민의 일상 언어로 설명합니다. 진단이나 치료를 대신하지 않으며, 논문이 말한 사실과 아직 알 수 없는 한계를 함께 살핍니다.</p>
  <div class="cta-row">
    <a class="button" href="{{ '/about/' | relative_url }}">뉴로시민 소개</a>
    <a class="button ghost" href="#latest">최신 글 보기</a>
  </div>
  <figure class="hero-visual">
    <img src="{{ '/assets/images/hero/neuroscience-hero.png' | relative_url }}" alt="배움과 감정, 습관을 뇌과학으로 이해하는 시민을 상징하는 이미지" loading="eager">
  </figure>
</section>

<section class="principles">
  <div><strong>연구 근거</strong><span>논문·학술지·PubMed 등 검증 가능한 출처를 확인합니다.</span></div>
  <div><strong>시민의 언어</strong><span>전문용어를 일상의 질문과 연결해 설명합니다.</span></div>
  <div><strong>배움과 마음</strong><span>부모·교사·학습자가 참고할 수 있는 판단 기준을 남깁니다.</span></div>
  <div><strong>안전한 이해</strong><span>과장된 결론과 의료적 단정을 피하고 한계를 함께 밝힙니다.</span></div>
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
