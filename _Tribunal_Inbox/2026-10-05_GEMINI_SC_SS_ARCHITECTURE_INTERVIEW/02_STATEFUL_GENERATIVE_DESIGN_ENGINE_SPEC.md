# Stateful Generative Design Engine: Mathematical & Combinatorial Brand Orchestration

**Document ID:** TRIBUNAL-SPEC-20261005-DESIGN-ENGINE-02  
**Authority:** DCS Level 0 Designation  
**Operating Framework:** DCSE Doctrine v7.3 Operative  
**Implementation Target:** ESCD Python Orchestrator (`apps/escd/`), Supabase (`dcse_cp`)

---

## 1. Architectural Philosophy: The Stateful Design Ledger

Traditional generative design engines suffer from two critical failure modes:
1. **Static Monotony:** Hardcoding 2–3 static hex codes creates repetitive, tired web assets across sibling products.
2. **Unchecked Hallucination:** Letting an LLM choose arbitrary colors and font sizes results in illegible contrast, broken layouts, and brand identity drift.

The DCS architectural breakthrough shifts web design from static templates to a **Stateful Generative Design Engine**. By treating color pools, typography ratios, and grid structures as mathematical variables governed by state ledgers, the system guarantees:
- **Infinite Variation without Fatigue:** Combinatorially generates unique visual palettes for each sub-entity.
- **Deterministic Accessibility:** Programmatically enforces Web Content Accessibility Guidelines (WCAG) 4.5:1 relative luminance contrast before any pairing is marked available.
- **Inventory Ledger Tracking:** Statefully records consumed vs. available palettes in a persistent database, preventing collisions across sibling entities.

---

## 2. Mathematical Components

### 2.1 Combinatorial Color Pools & WCAG Relative Luminance
Color combinations are generated as permutations of approved brand color spaces:
- **Sonly Consulting (SC):** Deep Corporate Blues, Victory Golds, Crisp White, Platinum Slate (`#0E2A47`, `#1A4068`, `#C89E4F`, `#D4AF37`, `#F8F9FC`, `#FFFFFF`).
- **Smoove Spots (SS):** Organic Deep Greens, Polished Silvers, Obsidian Charcoal, Emerald Accents (`#0A231C`, `#1B4332`, `#C0C0C0`, `#E5E5E5`, `#1A1A1A`, `#2D6A4F`).

The scientific contrast validation applies the W3C relative luminance formula:
$$L = 0.2126 \times R + 0.7152 \times G + 0.0722 \times B$$
where linearized color components $C \in \{R, G, B\}$ are calculated as:
$$C = \begin{cases} \frac{C_{\text{srgb}}}{12.92} & \text{if } C_{\text{srgb}} \le 0.03928 \\ \left(\frac{C_{\text{srgb}} + 0.055}{1.055}\right)^{2.4} & \text{otherwise} \end{cases}$$
The contrast ratio between background $L_1$ and foreground $L_2$ (where $L_1 > L_2$) is:
$$\text{Contrast Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}$$
Any permutation with $\text{Ratio} < 4.5$ is destroyed at the generation phase.

### 2.2 Modular Typography Scales
Arbitrary font sizing is prohibited. Heading scales are calculated via mathematical multipliers:
- **SC (Executive & Precise):** Minor Third ratio ($1.200$). Base: $16\text{px}$.
  - Body: $16.00\text{px}$
  - H5: $19.20\text{px}$
  - H4: $23.04\text{px}$
  - H3: $27.65\text{px}$
  - H2: $33.18\text{px}$
  - H1: $39.81\text{px}$
- **SS (Soulful & Cinematic):** Perfect Fourth ratio ($1.333$). Base: $16\text{px}$.
  - Body: $16.00\text{px}$
  - H5: $21.33\text{px}$
  - H4: $28.43\text{px}$
  - H3: $37.90\text{px}$
  - H2: $50.52\text{px}$
  - H1: $67.35\text{px}$

### 2.3 Layout Grid Archetypes
Layouts conform to an 8-pixel spacing system on a 12-column responsive grid:
- **Archetype A (The Bento Box):** 12-column grid divided into asymmetrical cards (8-col hero, 4-col sidebar, modular sub-cards).
- **Archetype B (The Cinematic Scroll):** 1-column reading rail with an $800\text{px}$ max-width constraint for immersive storytelling.
- **Archetype C (The Executive Dashboard):** 3-column equal split ($4\times 4\times 4$) for CaaS pricing tiers, audit matrices, and diagnostic metrics.

---

## 3. Production Python Implementation

```python
"""
DCSE Stateful Generative Design Engine
Orchestrates Color, Typography, and Layout statefully for SC and SS web entities.
"""

import itertools
import json
import math
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# BRAND TOKEN SPECIFICATIONS
# ---------------------------------------------------------------------------
BRAND_TOKENS = {
    "SC": {
        "name": "Sonly Consulting",
        "base_font_px": 16,
        "scale_ratio": 1.200,  # Minor Third (Executive, Controlled)
        "color_pool": [
            "#0E2A47",  # Deep Navy
            "#1A4068",  # Slate Blue
            "#C89E4F",  # Victory Gold
            "#D4AF37",  # Metallic Gold
            "#F8F9FC",  # Off-White Base
            "#FFFFFF",  # Pure White
        ],
        "font_pairings": [
            {"heading": "Inter", "body": "Roboto"},
            {"heading": "Helvetica Neue", "body": "Arial"},
            {"heading": "Cinzel", "body": "Plus Jakarta Sans"},
        ],
        "allowed_layouts": [
            "Executive_Dashboard",
            "Bento_Box_Asymmetric",
            "Split_8_4",
            "Lateral_Card_Flow",
        ],
    },
    "SS": {
        "name": "Smoove Spots",
        "base_font_px": 16,
        "scale_ratio": 1.333,  # Perfect Fourth (Dramatic, Cinematic)
        "color_pool": [
            "#0A231C",  # Deep Forest Green
            "#1B4332",  # Pine Green
            "#C0C0C0",  # Polished Silver
            "#E5E5E5",  # Platinum
            "#1A1A1A",  # Charcoal Obsidian
            "#2D6A4F",  # Vibrant Emerald
        ],
        "font_pairings": [
            {"heading": "Playfair Display", "body": "Lora"},
            {"heading": "Cormorant Garamond", "body": "Merriweather"},
            {"heading": "Cinzel", "body": "Inter"},
        ],
        "allowed_layouts": [
            "Cinematic_Scroll",
            "Bento_Box_Asymmetric",
            "Hero_Full_Bleed",
            "Lateral_Card_Flow",
        ],
    },
}

# ---------------------------------------------------------------------------
# SCIENTIFIC ACCESSIBILITY FUNCTIONS (WCAG 2.1 RELATIVE LUMINANCE)
# ---------------------------------------------------------------------------
def _hex_to_srgb(hex_color: str) -> Tuple[float, float, float]:
    """Converts 6-character hex color to normalized sRGB floats (0.0 to 1.0)."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color format: {hex_color}")
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def _calculate_channel_luminance(c: float) -> float:
    """Applies gamma linearization for WCAG relative luminance calculation."""
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def calculate_relative_luminance(hex_color: str) -> float:
    """Calculates relative luminance according to W3C standard."""
    r, g, b = _hex_to_srgb(hex_color)
    return (
        0.2126 * _calculate_channel_luminance(r)
        + 0.7152 * _calculate_channel_luminance(g)
        + 0.0722 * _calculate_channel_luminance(b)
    )

def calculate_wcag_contrast(hex_bg: str, hex_text: str) -> float:
    """
    Calculates contrast ratio between background and text colors.
    Returns value between 1.0 (no contrast) and 21.0 (max contrast).
    """
    l1 = calculate_relative_luminance(hex_bg)
    l2 = calculate_relative_luminance(hex_text)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

# ---------------------------------------------------------------------------
# TYPOGRAPHY SCALE GENERATION
# ---------------------------------------------------------------------------
def generate_type_scale(base: float, ratio: float, levels: int = 5) -> Dict[str, float]:
    """Generates mathematical type scale from Body up to H1."""
    scale = {"body": round(base, 2)}
    current_size = base
    for i in range(1, levels + 1):
        current_size *= ratio
        scale[f"H{6 - i}"] = round(current_size, 2)
    return scale

# ---------------------------------------------------------------------------
# STATEFUL ORCHESTRATOR ENGINE
# ---------------------------------------------------------------------------
class StatefulDesignEngine:
    def __init__(self, ledger_path: str = "design_state_ledger.json"):
        self.ledger_path = ledger_path
        self.state = self._load_ledger()

    def _load_ledger(self) -> Dict:
        try:
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"entities": {}, "consumed_palettes": {}, "consumed_layouts": {}}

    def _save_ledger(self):
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def allocate_page_design(
        self,
        entity_key: str,
        page_id: str,
        require_contrast: float = 4.5,
    ) -> Dict:
        """
        Allocates a mathematically valid, unique design package (colors, type, layout)
        and commits the allocation to the persistent state ledger.
        """
        if entity_key not in BRAND_TOKENS:
            raise KeyError(f"Unknown entity key: {entity_key}. Allowed: SC, SS")

        tokens = BRAND_TOKENS[entity_key]
        consumed_palettes = set(self.state["consumed_palettes"].get(entity_key, []))
        consumed_layouts = set(self.state["consumed_layouts"].get(entity_key, []))

        # 1. Select accessible, unconsumed color palette (bg, text, accent)
        selected_palette = None
        for bg, text, accent in itertools.permutations(tokens["color_pool"], 3):
            # Check text accessibility against background
            if calculate_wcag_contrast(bg, text) >= require_contrast:
                palette_id = f"{bg}:{text}:{accent}"
                if palette_id not in consumed_palettes:
                    selected_palette = {
                        "palette_id": palette_id,
                        "background": bg,
                        "text": text,
                        "accent": accent,
                        "contrast_ratio": round(calculate_wcag_contrast(bg, text), 2),
                    }
                    break

        if not selected_palette:
            raise RuntimeError(f"All WCAG-compliant color permutations exhausted for {entity_key}")

        # 2. Select unconsumed typography pairing & layout archetype
        selected_layout_bundle = None
        for font in tokens["font_pairings"]:
            for layout in tokens["allowed_layouts"]:
                layout_id = f"{font['heading']}:{layout}"
                if layout_id not in consumed_layouts:
                    selected_layout_bundle = {
                        "layout_id": layout_id,
                        "font_pairing": font,
                        "layout_archetype": layout,
                        "type_scale": generate_type_scale(tokens["base_font_px"], tokens["scale_ratio"]),
                    }
                    break
            if selected_layout_bundle:
                break

        if not selected_layout_bundle:
            raise RuntimeError(f"All typography/layout permutations exhausted for {entity_key}")

        # 3. Commit allocation to ledger
        if entity_key not in self.state["consumed_palettes"]:
            self.state["consumed_palettes"][entity_key] = []
            self.state["consumed_layouts"][entity_key] = []
            self.state["entities"][entity_key] = {}

        self.state["consumed_palettes"][entity_key].append(selected_palette["palette_id"])
        self.state["consumed_layouts"][entity_key].append(selected_layout_bundle["layout_id"])
        
        allocation_record = {
            "entity": entity_key,
            "page_id": page_id,
            "palette": selected_palette,
            "typography_and_layout": selected_layout_bundle,
            "status": "ALLOCATED_AND_LOCKED",
        }
        self.state["entities"][entity_key][page_id] = allocation_record
        self._save_ledger()

        return allocation_record
```

---

## 4. Supabase Schema for Production Persistence

To migrate the ledger from a local JSON file to the `dcse_cp` schema in Supabase:

```sql
-- Schema: dcse_cp
-- Table: design_token_allocations

CREATE TABLE IF NOT EXISTS dcse_cp.design_token_allocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_key VARCHAR(10) NOT NULL CHECK (entity_key IN ('SC', 'SS', 'PS', 'TSL', 'DCSE')),
    page_id VARCHAR(100) NOT NULL,
    palette_id VARCHAR(100) NOT NULL,
    background_hex VARCHAR(7) NOT NULL,
    text_hex VARCHAR(7) NOT NULL,
    accent_hex VARCHAR(7) NOT NULL,
    contrast_ratio NUMERIC(4, 2) NOT NULL CHECK (contrast_ratio >= 4.5),
    heading_font VARCHAR(50) NOT NULL,
    body_font VARCHAR(50) NOT NULL,
    layout_archetype VARCHAR(50) NOT NULL,
    scale_ratio NUMERIC(5, 3) NOT NULL,
    type_scale_json JSONB NOT NULL,
    status VARCHAR(30) DEFAULT 'ALLOCATED_AND_LOCKED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entity_key, page_id),
    UNIQUE(entity_key, palette_id)
);

CREATE INDEX IF NOT EXISTS idx_design_tokens_entity ON dcse_cp.design_token_allocations(entity_key);
```
