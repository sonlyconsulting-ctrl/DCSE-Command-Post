#!/usr/bin/env python3
"""
DCSE Persona Web Set Builder
Task ID: DCSE-PERSONA-WEBSET-20260915-01

Loads the governed 17-row persona matrix and generates:
1. Reusable Atlas index page (personas/index.html)
2. 17 persona detail routes (personas/<slug>/index.html)

Strictly enforces D10 separation: Internal D10 identities are NEVER rendered into public HTML.
"""

import os
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MATRIX_PATH = BASE_DIR / "governance" / "v7.2" / "personas" / "PERSONA_GOVERNED_MATRIX_V1.json"
APPS_DIR = BASE_DIR / "apps" / "personas"
OUTPUT_DIR = BASE_DIR / "personas"

DETAIL_TEMPLATE_PATH = APPS_DIR / "template.html"
ATLAS_TEMPLATE_PATH = APPS_DIR / "atlas_template.html"

def load_matrix():
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"Missing matrix file: {MATRIX_PATH}")
    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["personas"]

def render_pathways(pathways):
    items = []
    for path in pathways:
        label = path.strip("/").replace("-", " ").title()
        items.append(f'<li class="pathway-item"><a href="#{path}"><span>&rarr;</span> {label}</a></li>')
    return "\n          ".join(items)

def build_detail_page(persona, template_str):
    html = template_str
    html = html.replace("{{public_nickname}}", persona["public_nickname"])
    html = html.replace("{{public_slug}}", persona["public_slug"])
    html = html.replace("{{essence}}", persona["essence"])
    html = html.replace("{{cluster_label}}", persona["cluster_label"])
    html = html.replace("{{svg_icon}}", persona["svg_icon"])
    html = html.replace("{{intended_outcome}}", persona["intended_outcome"])
    html = html.replace("{{motivations}}", persona["motivations"])
    html = html.replace("{{frictions}}", persona["frictions"])
    html = html.replace("{{interaction_style}}", persona["interaction_style"])
    html = html.replace("{{tech_media_preference}}", persona["tech_media_preference"])
    html = html.replace("{{trust_factors}}", persona["trust_factors"])
    html = html.replace("{{avoid_factors}}", persona["avoid_factors"])
    html = html.replace("{{move_forward_guidance}}", persona["move_forward_guidance"])
    html = html.replace("{{public_safe_status}}", persona["public_safe_status"])
    html = html.replace("{{visual_state}}", persona["visual_state"])
    
    pathways_html = render_pathways(persona["relevant_governed_pathways"])
    html = html.replace("{{pathways_html}}", pathways_html)
    return html

def build_atlas_card(persona):
    slug = persona["public_slug"]
    return f"""      <article class="persona-card" data-cluster="{persona['cluster']}" tabindex="0" aria-label="{persona['public_nickname']}">
        <div class="card-header">
          <div class="avatar-wrapper" aria-hidden="true">
            {persona['svg_icon']}
          </div>
          <div class="header-text">
            <span class="cluster-tag">{persona['cluster_label']}</span>
            <h2 class="nickname">{persona['public_nickname']}</h2>
          </div>
        </div>
        <div class="essence-quote">
          "{persona['essence']}"
        </div>
        <div class="meta-list">
          <div class="meta-row">
            <span class="meta-label">Motivated By</span>
            <span class="meta-value">{persona['motivations']}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">Friction</span>
            <span class="meta-value">{persona['frictions']}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">Style</span>
            <span class="meta-value">{persona['interaction_style']}</span>
          </div>
        </div>
        <div class="forward-box">
          <div class="forward-box-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            What Helps Them Move Forward
          </div>
          <p>{persona['move_forward_guidance']}</p>
        </div>
        <a href="./{slug}/index.html" class="card-footer-cta" aria-label="Explore {persona['public_nickname']} detail profile">
          <span>Explore Detail Profile</span>
          <span class="arrow">&rarr;</span>
        </a>
      </article>"""

def main():
    personas = load_matrix()
    if len(personas) != 17:
        raise ValueError(f"Expected 17 personas in matrix, got {len(personas)}")

    with open(DETAIL_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        detail_template_str = f.read()

    with open(ATLAS_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        atlas_template_str = f.read()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Build 17 detail pages
    detail_routes = []
    for p in personas:
        slug = p["public_slug"]
        slug_dir = OUTPUT_DIR / slug
        slug_dir.mkdir(parents=True, exist_ok=True)
        rendered_html = build_detail_page(p, detail_template_str)
        out_file = slug_dir / "index.html"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        detail_routes.append(str(out_file))

    print(f"Generated {len(detail_routes)} detail persona pages.")

    # 2. Build Atlas index page
    card_htmls = [build_atlas_card(p) for p in personas]
    grid_items = "\n\n".join(card_htmls)
    atlas_html = atlas_template_str.replace("{{grid_items_html}}", grid_items)
    atlas_out = OUTPUT_DIR / "index.html"
    with open(atlas_out, "w", encoding="utf-8") as f:
        f.write(atlas_html)
    print(f"Generated Atlas landing page: {atlas_out}")

if __name__ == "__main__":
    main()
