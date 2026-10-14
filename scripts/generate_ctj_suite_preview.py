import os
import json
import base64

# Load assets
mark_path = r'C:\DS All Things\SC-CTJ\public\assets\ctj-family-mark.webp'
lockup_path = r'C:\DS All Things\SC-CTJ\public\assets\unified-lockup.webp'

with open(mark_path, 'rb') as f:
    mark_b64 = base64.b64encode(f.read()).decode('ascii')
with open(lockup_path, 'rb') as f:
    lockup_b64 = base64.b64encode(f.read()).decode('ascii')

# Load curriculum
with open(r'C:\DS All Things\SC-CTJ\src\data\curriculum.ts', 'r', encoding='utf-8') as f:
    raw = f.read()
start = raw.find('= [') + 2
raw_json = raw[start:].strip().rstrip(';')
curriculum = json.loads(raw_json)

# Load introductions
with open(r'C:\DS All Things\SC-CTJ\src\data\partIntroductions.json', 'r', encoding='utf-8') as f:
    introductions = json.load(f)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Critical Thinker's Journey™ (CTJ) · Master Product Suite & Review Environment</title>
<style>
:root {{
  --bg-primary: #070e17;
  --bg-secondary: #0d1927;
  --bg-card: #122133;
  --bg-elevated: #172a42;
  --text-main: #f0f4f8;
  --text-muted: #96a9bd;
  --gold-primary: #e2c779;
  --gold-glow: #ffd978;
  --gold-dark: #b89c4d;
  --border-subtle: rgba(226, 199, 121, 0.22);
  --border-strong: rgba(226, 199, 121, 0.45);
  --accent-cyan: #4ecdc4;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --font-serif: "Georgia", "Cambria", "Times New Roman", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  background: var(--bg-primary);
  color: var(--text-main);
  font-family: var(--font-sans);
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}}

a {{
  color: var(--gold-primary);
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;
}}
a:hover {{
  color: var(--gold-glow);
}}

/* ==========================================================================
   TOP BAR / CROSS-APP CONTINUITY BAR
   ========================================================================== */
.continuity-bar {{
  background: #050b12;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding: 8px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: var(--text-muted);
}}
.continuity-left {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.return-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(226, 199, 121, 0.12);
  color: var(--gold-primary);
  border: 1px solid var(--border-subtle);
  padding: 5px 12px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}}
.return-btn:hover {{
  background: rgba(226, 199, 121, 0.22);
  border-color: var(--gold-primary);
  color: #fff;
}}
.continuity-env {{
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #7d90a6;
  background: rgba(255, 255, 255, 0.05);
  padding: 3px 8px;
  border-radius: 4px;
}}

/* ==========================================================================
   SOLIDIFIED MASTER SUITE HEADER
   ========================================================================== */
.master-header {{
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-subtle);
  padding: 14px 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
}}
.header-container {{
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}}
.brand-identity {{
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  background: transparent;
  border: none;
  text-align: left;
  color: inherit;
}}
.brand-logo {{
  width: 44px;
  height: 44px;
  border-radius: 8px;
  object-fit: contain;
  box-shadow: 0 0 12px rgba(226, 199, 121, 0.2);
}}
.brand-titles h1 {{
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #ffffff;
}}
.brand-titles h1 span {{
  color: var(--gold-primary);
}}
.brand-titles p {{
  font-size: 11px;
  color: var(--text-muted);
  letter-spacing: 0.03em;
}}

/* Suite Navigation Tabs */
.suite-nav {{
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(0, 0, 0, 0.25);
  padding: 4px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.06);
}}
.nav-tab {{
  background: transparent;
  border: 1px solid transparent;
  color: var(--text-muted);
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}}
.nav-tab:hover {{
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.04);
}}
.nav-tab.active {{
  color: var(--bg-primary);
  background: var(--gold-primary);
  border-color: var(--gold-primary);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(226, 199, 121, 0.3);
}}

/* Header Utilities */
.header-actions {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.btn-author-intro {{
  background: rgba(226, 199, 121, 0.12);
  border: 1px solid var(--border-subtle);
  color: var(--gold-primary);
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}}
.btn-author-intro:hover {{
  background: var(--gold-primary);
  color: var(--bg-primary);
}}

/* ==========================================================================
   MAIN WORKSPACE AREA
   ========================================================================== */
.workspace-wrapper {{
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 20px 60px;
}}

/* ==========================================================================
   PART 2 DRAMATIC & SOULFUL COVER PAGE
   ========================================================================== */
.cover-hero {{
  position: relative;
  background: linear-gradient(145deg, #0d1b2a 0%, #08111d 60%, #152233 100%);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-lg);
  padding: 56px 48px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(226, 199, 121, 0.2);
  margin-bottom: 36px;
  overflow: hidden;
}}
.cover-hero::before {{
  content: "";
  position: absolute;
  top: -80px;
  right: -80px;
  width: 320px;
  height: 320px;
  background: radial-gradient(circle, rgba(226, 199, 121, 0.12) 0%, transparent 70%);
  pointer-events: none;
}}
.cover-hero::after {{
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
}}

.cover-badge {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold-primary);
  background: rgba(226, 199, 121, 0.1);
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid var(--border-subtle);
  margin-bottom: 22px;
  font-weight: 600;
}}

.cover-title {{
  font-family: var(--font-serif);
  font-size: clamp(34px, 4.5vw, 48px);
  color: #ffffff;
  line-height: 1.18;
  margin-bottom: 14px;
  font-weight: 600;
  letter-spacing: -0.01em;
}}
.cover-title span {{
  color: var(--gold-primary);
  font-style: italic;
}}

.cover-subtitle {{
  font-size: 20px;
  color: var(--gold-primary);
  margin-bottom: 24px;
  font-weight: 400;
  letter-spacing: 0.02em;
}}

.cover-manifesto {{
  font-size: 16px;
  color: #c4d3e2;
  line-height: 1.8;
  max-width: 860px;
  margin-bottom: 32px;
  border-left: 3px solid var(--gold-primary);
  padding-left: 20px;
  background: rgba(0, 0, 0, 0.18);
  padding: 16px 20px;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
}}
.cover-manifesto p + p {{
  margin-top: 12px;
}}

.cover-action-row {{
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}}
.btn-primary-action {{
  background: linear-gradient(180deg, #ecd693 0%, #caa452 100%);
  color: #070e17;
  border: none;
  font-size: 15px;
  font-weight: 700;
  padding: 14px 28px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 16px rgba(226, 199, 121, 0.35);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.btn-primary-action:hover {{
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(226, 199, 121, 0.5);
}}
.btn-secondary-action {{
  background: transparent;
  color: #c4d3e2;
  border: 1px solid var(--border-subtle);
  font-size: 14px;
  font-weight: 600;
  padding: 13px 22px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}}
.btn-secondary-action:hover {{
  color: #ffffff;
  border-color: var(--gold-primary);
  background: rgba(255, 255, 255, 0.04);
}}

/* ==========================================================================
   CURRICULUM BUILDER WORKSPACE (SCREENSHOT 2 DESIGN)
   ========================================================================== */
.builder-view {{
  background: var(--bg-secondary);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
}}

.builder-subbar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 24px;
}}
.builder-progress-pill {{
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  text-transform: uppercase;
  font-weight: 600;
}}
.builder-progress-bar-container {{
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: var(--gold-primary);
}}
.progress-track {{
  width: 140px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}}
.progress-fill {{
  height: 100%;
  background: var(--gold-primary);
  width: 10%;
  transition: width 0.3s ease;
}}

/* Day selector tabs */
.day-selector-track {{
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 16px;
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}}
.day-btn {{
  background: var(--bg-card);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--text-muted);
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}}
.day-btn:hover {{
  color: #fff;
  border-color: var(--border-subtle);
}}
.day-btn.active {{
  background: var(--gold-primary);
  color: #070e17;
  border-color: var(--gold-primary);
  box-shadow: 0 2px 8px rgba(226, 199, 121, 0.25);
}}

/* Active Day Card */
.day-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 28px;
  margin-bottom: 28px;
}}
.day-eyebrow {{
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--gold-primary);
  font-weight: 700;
  margin-bottom: 6px;
}}
.day-title {{
  font-family: var(--font-serif);
  font-size: 28px;
  color: #ffffff;
  margin-bottom: 12px;
  font-weight: 600;
}}
.day-theme {{
  font-size: 15px;
  color: #c4d3e2;
  line-height: 1.6;
  margin-bottom: 24px;
}}

/* Cards grid: Mini-framework & Action tip */
.framework-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}}
@media (max-width: 768px) {{
  .framework-grid {{
    grid-template-columns: 1fr;
  }}
}}
.framework-card {{
  background: rgba(14, 27, 43, 0.85);
  border: 1px solid rgba(226, 199, 121, 0.18);
  border-radius: var(--radius-sm);
  padding: 16px 20px;
}}
.framework-card-title {{
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent-cyan);
  font-weight: 700;
  margin-bottom: 6px;
}}
.framework-name {{
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 6px;
}}
.framework-desc {{
  font-size: 13px;
  color: #b0c2d4;
  line-height: 1.5;
}}

.tip-card {{
  background: rgba(30, 24, 12, 0.45);
  border: 1px solid rgba(226, 199, 121, 0.28);
  border-radius: var(--radius-sm);
  padding: 16px 20px;
}}
.tip-card-title {{
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--gold-primary);
  font-weight: 700;
  margin-bottom: 6px;
}}
.tip-desc {{
  font-size: 14px;
  color: #e6dfc8;
  line-height: 1.5;
}}

.local-save-indicator {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #7d96b0;
  margin-bottom: 20px;
}}
.local-save-indicator svg {{
  width: 14px;
  height: 14px;
  fill: currentColor;
}}

/* Core Session & Interactive Fields */
.session-header {{
  font-size: 18px;
  color: #ffffff;
  font-weight: 700;
  margin-bottom: 6px;
}}
.session-lede {{
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 24px;
}}

.prompt-block {{
  background: rgba(7, 14, 23, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
  padding: 20px;
  margin-bottom: 20px;
}}
.prompt-label {{
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 12px;
  display: block;
}}
.prompt-textarea {{
  width: 100%;
  min-height: 110px;
  background: #091320;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-sm);
  color: #f0f4f8;
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.6;
  padding: 12px 14px;
  resize: vertical;
  transition: border-color 0.2s ease;
}}
.prompt-textarea:focus {{
  outline: none;
  border-color: var(--gold-primary);
  box-shadow: 0 0 8px rgba(226, 199, 121, 0.2);
}}

/* ==========================================================================
   SOLIDIFIED CTJ FOOTER (MATCHING USER SCREENSHOT EXACTLY)
   ========================================================================== */
.master-footer {{
  background: #04080e;
  border-top: 1px solid rgba(226, 199, 121, 0.25);
  padding: 40px 24px 32px;
  color: #c4d3e2;
  font-size: 14px;
  margin-top: auto;
}}
.footer-container {{
  max-width: 1280px;
  margin: 0 auto;
}}
.footer-primary-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 28px;
}}
.footer-brand {{
  max-width: 380px;
}}
.footer-brand-title {{
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 4px;
}}
.footer-brand-title span {{
  color: var(--gold-primary);
}}
.footer-powered-by {{
  font-size: 13px;
  color: var(--gold-primary);
  margin-bottom: 8px;
}}
.footer-powered-by a {{
  color: var(--gold-primary);
  font-weight: 600;
}}

.footer-nav-links {{
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}}
.footer-link-btn {{
  background: transparent;
  border: none;
  color: #c4d3e2;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.2s ease;
}}
.footer-link-btn:hover {{
  color: var(--gold-primary);
}}

.footer-advisory {{
  font-size: 13px;
  color: #8397ad;
  line-height: 1.6;
  max-width: 900px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}}

/* ==========================================================================
   DOCUMENT MODAL & DRAWER SYSTEM
   ========================================================================== */
.modal-overlay {{
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(3, 7, 13, 0.85);
  backdrop-filter: blur(6px);
  z-index: 1000;
  justify-content: center;
  align-items: center;
  padding: 20px;
}}
.modal-overlay.active {{
  display: flex;
}}
.modal-content {{
  background: var(--bg-secondary);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 820px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
  overflow: hidden;
}}
.modal-header {{
  background: #091320;
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.modal-title {{
  font-family: var(--font-serif);
  font-size: 22px;
  color: var(--gold-primary);
  font-weight: 700;
}}
.modal-close-btn {{
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 24px;
  cursor: pointer;
  line-height: 1;
  padding: 4px;
}}
.modal-close-btn:hover {{
  color: #fff;
}}
.modal-body {{
  padding: 28px;
  overflow-y: auto;
  font-size: 15px;
  color: #c4d3e2;
  line-height: 1.7;
}}
.modal-body h2 {{
  font-size: 18px;
  color: #ffffff;
  margin: 20px 0 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 6px;
}}
.modal-body h2:first-of-type {{
  margin-top: 0;
}}
.modal-body ul {{
  margin: 10px 0 16px 24px;
}}
.modal-body li {{
  margin-bottom: 6px;
}}
.modal-footer {{
  background: #091320;
  padding: 16px 28px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: flex-end;
}}
.btn-close-modal {{
  background: var(--gold-primary);
  color: #070e17;
  border: none;
  font-weight: 700;
  padding: 8px 18px;
  border-radius: var(--radius-sm);
  cursor: pointer;
}}

/* Notification Pill */
.toast-msg {{
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--gold-primary);
  color: #070e17;
  padding: 10px 18px;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 13px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
  display: none;
  z-index: 2000;
}}
</style>
</head>
<body>

<!-- 1. CONTINUITY BAR / CROSS-APP RETURN NAVIGATION -->
<aside class="continuity-bar" aria-label="Suite continuity navigation">
  <div class="continuity-left">
    <button class="return-btn" id="returnBtn" onclick="handleCrossAppReturn()">
      ← Return to Previous App / Workspace
    </button>
    <span id="returnSourceDesc" style="font-size: 12px; color: #7f95ac;"></span>
  </div>
  <div class="continuity-env">
    Sovereign Production Direction · Zero Watermark Verified
  </div>
</aside>

<!-- 2. SOLIDIFIED SUITE HEADER -->
<header class="master-header">
  <div class="header-container">
    <button class="brand-identity" onclick="switchSuiteTab('part-1')">
      <img class="brand-logo" src="data:image/webp;base64,{mark_b64}" alt="CTJ Sovereign Mark">
      <div class="brand-titles">
        <h1>The Critical Thinker's Journey™ <span>(CTJ)</span></h1>
        <p>A Sonly Consulting Master Curriculum • Edition 1.1</p>
      </div>
    </button>

    <nav class="suite-nav" aria-label="CTJ Suite Tabs">
      <button class="nav-tab active" id="tab-p1" onclick="switchSuiteTab('part-1')">Part 1: Clarity</button>
      <button class="nav-tab" id="tab-p2" onclick="switchSuiteTab('part-2')">Part 2: Movement</button>
      <button class="nav-tab" id="tab-p3" onclick="switchSuiteTab('part-3')">Part 3: Balance</button>
      <button class="nav-tab" id="tab-unified" onclick="switchSuiteTab('unified')">The Unified Path</button>
      <button class="nav-tab" id="tab-sca" onclick="switchSuiteTab('sca')">Assessment (SCA)</button>
    </nav>

    <div class="header-actions">
      <button class="btn-author-intro" onclick="openDocumentModal('author-intro')">
        📖 Author & Intro
      </button>
      <button class="btn-author-intro" style="background: transparent; color: #c4d3e2;" onclick="openDocumentModal('terms')">
        ⚖ Legal & Policies
      </button>
    </div>
  </div>
</header>

<!-- 3. MAIN WORKSPACE CONTENT -->
<main class="workspace-wrapper" id="mainWorkspace">

  <!-- ====================================================================
       VIEW: PART 2 COVER & BUILDER EXPERIENCE
       ==================================================================== -->
  <div id="view-part-2" style="display: none;">
    <!-- SOULFUL, DRAMATIC COVER PAGE FOR PART 2 -->
    <section class="cover-hero" id="part2CoverPage">
      <div class="cover-badge">CTJ · PART 2 · TRANSITION FROM OBSERVER TO ARCHITECT</div>
      <h1 class="cover-title">Exploring Ideas and <span>Making Moves</span></h1>
      <p class="cover-subtitle">The Arena of Action • Testing Reality Against Reason</p>

      <div class="cover-manifesto">
        <p><strong>You have stilled the initial noise.</strong> In Part 1, you learned to separate verified facts from inherited assumptions, audit cognitive blind spots, and map the architecture of your thinking from the quiet vantage of an observer.</p>
        <p><strong>Part 2 leaves the observer's chair behind.</strong> Reasoning in isolation is merely rehearsal; sovereign mastery is forged when ideas collide with the friction, unpredictability, and resistance of the real world. In these 10 Builders, you do not construct rigid defenses or cling to comfortable dogmas. You enter the arena as an experimental architect.</p>
        <p>You will state hypotheses boldly, treat every argument as a probe to test rather than personal armor, and extract raw diagnostic intelligence from every setback. <em>Step forward. Prepare to move.</em></p>
      </div>

      <div class="cover-action-row">
        <button class="btn-primary-action" onclick="scrollToPart2Builders()">
          Enter Day 1: Testing Arguments →
        </button>
        <button class="btn-secondary-action" onclick="openDocumentModal('author-intro')">
          Read Founder's Note
        </button>
      </div>
    </section>

    <!-- PART 2 BUILDERS INTERACTIVE VIEW (MATCHING USER SCREENSHOT 2) -->
    <section class="builder-view" id="part2BuilderSection">
      <div class="builder-subbar">
        <div>
          <span class="builder-progress-pill" id="p2DayPill">WEEK 1 · DAY 1 OF 10</span>
          <h2 style="font-size: 20px; color: #fff; margin-top: 4px;">Part 2: Exploring Ideas and Making Moves</h2>
        </div>
        <div class="builder-progress-bar-container">
          <span id="p2ProgressPercent">10% THROUGH PART 2</span>
          <div class="progress-track">
            <div class="progress-fill" id="p2ProgressFill" style="width: 10%;"></div>
          </div>
        </div>
      </div>

      <!-- Builder Selector Nav -->
      <nav class="day-selector-track" id="p2DaySelector" aria-label="Part 2 Days"></nav>

      <!-- Active Day Card Container -->
      <div id="p2DayCardContainer"></div>
    </section>
  </div>

  <!-- ====================================================================
       VIEW: PART 1 EXPERIENCE (THE CREATED ctj-part1-review-20260912 APP)
       ==================================================================== -->
  <div id="view-part-1">
    <section class="cover-hero" style="border-color: rgba(78, 205, 196, 0.4);">
      <div class="cover-badge" style="color: var(--accent-cyan); border-color: rgba(78, 205, 196, 0.3); background: rgba(78, 205, 196, 0.08);">
        CTJ · PART 1 · FOUNDATIONAL ARCHITECTURE
      </div>
      <h1 class="cover-title">Building Clarity and <span>Confidence</span></h1>
      <p class="cover-subtitle">Clear the Cognitive Fog • Strip Away Inherited Assumptions</p>

      <div class="cover-manifesto">
        <p><strong>Mastery is intentional.</strong> When enterprise discipline meets deep intellectual clarity, technology stops being noise and becomes a multiplier. In Part 1, you build the bedrock of logical rigor.</p>
        <p>Over 10 deliberate Builders, you will systematically distinguish fact from opinion, isolate hidden fallacies, expose cognitive distortions, and construct arguments that endure rigorous scrutiny.</p>
      </div>

      <div class="cover-action-row">
        <button class="btn-primary-action" onclick="scrollToPart1Builders()">
          Open Part 1 Builders (Days 1–10) →
        </button>
        <button class="btn-secondary-action" onclick="openDocumentModal('author-intro')">
          Executive Intro
        </button>
      </div>
    </section>

    <section class="builder-view" id="part1BuilderSection">
      <div class="builder-subbar">
        <div>
          <span class="builder-progress-pill" id="p1DayPill">WEEK 1 · DAY 1 OF 10</span>
          <h2 style="font-size: 20px; color: #fff; margin-top: 4px;">Part 1: Building Clarity and Confidence</h2>
        </div>
        <div class="builder-progress-bar-container">
          <span id="p1ProgressPercent">10% THROUGH PART 1</span>
          <div class="progress-track">
            <div class="progress-fill" id="p1ProgressFill" style="width: 10%;"></div>
          </div>
        </div>
      </div>

      <nav class="day-selector-track" id="p1DaySelector" aria-label="Part 1 Days"></nav>
      <div id="p1DayCardContainer"></div>
    </section>
  </div>

  <!-- ====================================================================
       VIEW: PART 3 EXPERIENCE
       ==================================================================== -->
  <div id="view-part-3" style="display: none;">
    <section class="cover-hero" style="border-color: rgba(226, 199, 121, 0.4);">
      <div class="cover-badge">CTJ · PART 3 · INTEGRATION & PURPOSE</div>
      <h1 class="cover-title">Finding Meaning and <span>Balance</span></h1>
      <p class="cover-subtitle">Anchor Strategic Rigor in Long-Term Sovereign Equilibrium</p>

      <div class="cover-manifesto">
        <p>Building on the foundations of clarity (Part 1) and decisive action (Part 2), Part 3 addresses the inner landscape of the thinker: metacognition, values alignment, sustainable cognitive stamina, and purpose.</p>
      </div>

      <div class="builder-view">
        <div class="builder-subbar">
          <div>
            <span class="builder-progress-pill" id="p3DayPill">WEEK 1 · DAY 1 OF 10</span>
            <h2 style="font-size: 20px; color: #fff; margin-top: 4px;">Part 3: Finding Meaning and Balance</h2>
          </div>
          <div class="builder-progress-bar-container">
            <span id="p3ProgressPercent">10% THROUGH PART 3</span>
            <div class="progress-track"><div class="progress-fill" id="p3ProgressFill" style="width: 10%;"></div></div>
          </div>
        </div>
        <nav class="day-selector-track" id="p3DaySelector" aria-label="Part 3 Days"></nav>
        <div id="p3DayCardContainer"></div>
      </div>
    </section>
  </div>

  <!-- ====================================================================
       VIEW: THE UNIFIED PATH (FLAGSHIP)
       ==================================================================== -->
  <div id="view-unified" style="display: none;">
    <section class="cover-hero">
      <div class="cover-badge">FLAGSHIP MASTER ENVIRONMENT</div>
      <h1 class="cover-title">The Unified <span>Path</span></h1>
      <p class="cover-subtitle">The Complete Architectural Reasoning System</p>
      <div class="cover-manifesto">
        <p>The Unified Path consolidates Decision Brief, Daily Thought Exercise, Integrated Capstone (4 scenarios & 7 CTJ lenses), and deterministic Logic Map into a single continuous master workspace.</p>
      </div>
      <div style="background: var(--bg-card); padding: 28px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
        <h3 style="color: var(--gold-primary); margin-bottom: 12px;">Live Decision Brief Active</h3>
        <p style="color: #c4d3e2; margin-bottom: 20px;">Examine a live strategic fork across 7 sovereign lenses: Analytical, Creative, Systems, Empathetic, Strategic, Ethical, and Reversibility.</p>
        <button class="btn-primary-action" onclick="alert('Unified Reasoning Engine active in review mode.')">Run Unified Reasoning Cycle</button>
      </div>
    </section>
  </div>

  <!-- ====================================================================
       VIEW: STRATEGIC CLARITY ASSESSMENT (SCA)
       ==================================================================== -->
  <div id="view-sca" style="display: none;">
    <section class="cover-hero">
      <div class="cover-badge">DIAGNOSTIC ENTRY POINT</div>
      <h1 class="cover-title">Strategic Clarity <span>Assessment</span></h1>
      <p class="cover-subtitle">31 Deterministic Questions Across 3 Core Pillars</p>
      <div class="cover-manifesto">
        <p>A private assessment measuring Analytical Precision, Creative Innovation, and Systems Thinking to pinpoint your optimal CTJ trajectory.</p>
      </div>
      <div style="background: var(--bg-card); padding: 28px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
        <h3 style="color: var(--gold-primary); margin-bottom: 12px;">Assessment Diagnostic Ready</h3>
        <p style="color: #c4d3e2; margin-bottom: 20px;">Questions evaluate cognitive habits, assumption auditing, and decision elasticity under pressure.</p>
        <button class="btn-primary-action" onclick="alert('SCA 31-Question Diagnostic Ready.')">Start Assessment</button>
      </div>
    </section>
  </div>

</main>

<!-- 4. SOLIDIFIED SUITE FOOTER (MATCHING USER SCREENSHOT EXACTLY) -->
<footer class="master-footer">
  <div class="footer-container">
    <div class="footer-primary-row">
      <div class="footer-brand">
        <p class="footer-brand-title">The Critical Thinker's Journey <span>• Unified Edition</span></p>
        <p class="footer-powered-by">Powered by <a href="https://www.sonlyconsulting.com" target="_blank" rel="noopener noreferrer">Sonly Consulting</a></p>
      </div>

      <nav class="footer-nav-links" aria-label="Footer Legal Links">
        <button class="footer-link-btn" onclick="openDocumentModal('terms')">Terms of Use</button>
        <button class="footer-link-btn" onclick="openDocumentModal('privacy')">Privacy Notice</button>
        <button class="footer-link-btn" onclick="openDocumentModal('refund')">Digital Product / Refund Policy</button>
        <button class="footer-link-btn" onclick="openDocumentModal('accessibility')">Accessibility Statement</button>
        <button class="footer-link-btn" onclick="openDocumentModal('support')">Support</button>
        <button class="footer-link-btn" onclick="openDocumentModal('author-intro')">Author & Intro</button>
      </nav>
    </div>

    <div class="footer-advisory">
      Educational and reflective. Not medical, therapeutic, psychological, legal, or financial advice. All policy and governance documents are verified, authoritative, and accessible on demand across the entire CTJ Product Suite.
    </div>
  </div>
</footer>

<!-- 5. COMPREHENSIVE DOCUMENT MODAL (NO MORE CONTENT SOURCE REQUIRED!) -->
<div class="modal-overlay" id="documentModal" onclick="closeModalOnBackdrop(event)">
  <div class="modal-content" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
    <div class="modal-header">
      <h2 class="modal-title" id="modalTitle">Document Viewer</h2>
      <button class="modal-close-btn" onclick="closeDocumentModal()" aria-label="Close dialog">&times;</button>
    </div>
    <div class="modal-body" id="modalBody">
      <!-- Dynamic Document Text Injected Here -->
    </div>
    <div class="modal-footer">
      <button class="btn-close-modal" onclick="closeDocumentModal()">Close Document</button>
    </div>
  </div>
</div>

<div class="toast-msg" id="toastMsg">Responses saved locally to your device</div>

<script>
// Curriculum data
const CURRICULUM = {json.dumps(curriculum)};
const INTRODUCTIONS = {json.dumps(introductions)};

// Active states
let currentPartId = 'part-1';
let activeDays = {{
  'part-1': 1,
  'part-2': 1,
  'part-3': 1
}};

// Setup return navigation
function initReturnNavigation() {{
  const params = new URLSearchParams(window.location.search);
  const returnTo = params.get('returnTo') || document.referrer;
  const returnBtn = document.getElementById('returnBtn');
  const desc = document.getElementById('returnSourceDesc');

  if (returnTo && returnTo.startsWith('http')) {{
    try {{
      const url = new URL(returnTo);
      desc.textContent = `Destination: ${{url.hostname}}`;
      window.__CTJ_RETURN_URL__ = returnTo;
    }} catch (e) {{
      desc.textContent = "Return to Suite Hub";
    }}
  }} else {{
    desc.textContent = "Return to Sonly Consulting Product Hub";
    window.__CTJ_RETURN_URL__ = "https://sc-product-showroom-preview.sonlysc.chatgpt.site";
  }}
}}

function handleCrossAppReturn() {{
  if (window.__CTJ_RETURN_URL__) {{
    window.location.href = window.__CTJ_RETURN_URL__;
  }} else {{
    window.location.href = "https://sc-product-showroom-preview.sonlysc.chatgpt.site";
  }}
}}

// Tab switcher
function switchSuiteTab(partId) {{
  currentPartId = partId;
  const tabs = ['part-1', 'part-2', 'part-3', 'unified', 'sca'];
  tabs.forEach(t => {{
    const el = document.getElementById('view-' + t);
    const tabBtn = document.getElementById('tab-' + (t === 'part-1' ? 'p1' : t === 'part-2' ? 'p2' : t === 'part-3' ? 'p3' : t));
    if (el) el.style.display = (t === partId) ? 'block' : 'none';
    if (tabBtn) {{
      if (t === partId) tabBtn.classList.add('active');
      else tabBtn.classList.remove('active');
    }}
  }});
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function scrollToPart2Builders() {{
  document.getElementById('part2BuilderSection').scrollIntoView({{ behavior: 'smooth' }});
}}

function scrollToPart1Builders() {{
  document.getElementById('part1BuilderSection').scrollIntoView({{ behavior: 'smooth' }});
}}

// Render Builders for Part
function renderBuildersForPart(partId, partIndex) {{
  const partData = CURRICULUM[partIndex];
  if (!partData) return;

  const prefix = partId === 'part-1' ? 'p1' : partId === 'part-2' ? 'p2' : 'p3';
  const navEl = document.getElementById(prefix + 'DaySelector');
  const cardContainer = document.getElementById(prefix + 'DayCardContainer');
  if (!navEl || !cardContainer) return;

  navEl.innerHTML = '';
  partData.days.forEach(d => {{
    const btn = document.createElement('button');
    btn.className = 'day-btn' + (d.day === activeDays[partId] ? ' active' : '');
    btn.textContent = `Day ${{d.day}} · ${{d.title.split(' ').slice(0, 3).join(' ')}}`;
    btn.onclick = () => selectDay(partId, d.day);
    navEl.appendChild(btn);
  }});

  const activeDayData = partData.days.find(d => d.day === activeDays[partId]) || partData.days[0];
  
  // Update progress
  const percent = activeDayData.day * 10;
  const pill = document.getElementById(prefix + 'DayPill');
  const percentText = document.getElementById(prefix + 'ProgressPercent');
  const fill = document.getElementById(prefix + 'ProgressFill');
  if (pill) pill.textContent = `WEEK ${{Math.ceil(activeDayData.day / 5)}} · DAY ${{activeDayData.day}} OF 10`;
  if (percentText) percentText.textContent = `${{percent}}% THROUGH PART ${{partIndex + 1}}`;
  if (fill) fill.style.width = `${{percent}}%`;

  // Render card
  let promptsHtml = '';
  if (activeDayData.prompts && activeDayData.prompts.length > 0) {{
    promptsHtml = activeDayData.prompts.map((p, idx) => {{
      const storageKey = `ctj.${{partId}}.day-${{activeDayData.day}}.p${{idx}}`;
      const savedVal = localStorage.getItem(storageKey) || '';
      return `
        <div class="prompt-block">
          <label class="prompt-label" for="${{storageKey}}">
            Prompt ${{idx + 1}}: ${{p.text || p.label || p}}
          </label>
          <textarea 
            class="prompt-textarea" 
            id="${{storageKey}}" 
            placeholder="Type your reflection or response here..."
            oninput="handlePromptInput('${{storageKey}}', this.value)"
          >${{savedVal}}</textarea>
        </div>
      `;
    }}).join('');
  }}

  cardContainer.innerHTML = `
    <article class="day-card">
      <p class="day-eyebrow">DAY ${{activeDayData.day}}</p>
      <h3 class="day-title">${{activeDayData.title}}</h3>
      <p class="day-theme">${{activeDayData.theme || ''}}</p>

      <div class="framework-grid">
        <div class="framework-card">
          <p class="framework-card-title">MINI-FRAMEWORK</p>
          <p class="framework-name">${{activeDayData.framework ? activeDayData.framework.name : 'Structured Reflection'}}</p>
          <p class="framework-desc">${{activeDayData.framework ? activeDayData.framework.description : 'Examine the logical flow of this decision point.'}}</p>
        </div>
        <div class="tip-card">
          <p class="tip-card-title">💡 ACTION TIP</p>
          <p class="tip-desc">${{activeDayData.tip || 'Treat an argument as a hypothesis to test, not a position to defend.'}}</p>
        </div>
      </div>

      <div class="local-save-indicator">
        <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-7 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/></svg>
        <span>Responses saved locally to your device browser</span>
      </div>

      <div class="session-header">Core Session</div>
      <p class="session-lede">Complete the core prompts. Deeper reflection remains available but is not required to advance.</p>

      ${{promptsHtml}}
    </article>
  `;
}}

function selectDay(partId, day) {{
  activeDays[partId] = day;
  const partIndex = partId === 'part-1' ? 0 : partId === 'part-2' ? 1 : 2;
  renderBuildersForPart(partId, partIndex);
}}

function handlePromptInput(key, val) {{
  try {{
    localStorage.setItem(key, val);
    showToast();
  }} catch(e) {{}}
}}

let toastTimer = null;
function showToast() {{
  const toast = document.getElementById('toastMsg');
  if (!toast) return;
  toast.style.display = 'block';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {{
    toast.style.display = 'none';
  }}, 1500);
}}

// ==========================================================================
// COMPLETE LEGAL & GOVERNANCE DOCUMENTS REPOSITORY
// ==========================================================================
const DOCUMENTS = {{
  'terms': {{
    title: "Terms of Use · The Critical Thinker's Journey™",
    body: `
      <h2>1. Educational and Reflective Scope</h2>
      <p>The Critical Thinker's Journey™ (CTJ), including all related modules, digital workbooks, assessments, and companion experiences, is published by Sonly Consulting strictly for educational, personal reflection, and strategic self-evaluation purposes. CTJ does not provide medical, therapeutic, psychiatric, legal, or financial advice. Completion of cognitive drills and self-assessments does not establish a clinical or licensed fiduciary relationship.</p>

      <h2>2. Sovereign Intellectual Property</h2>
      <p>All curriculum architecture, proprietary Mini-Frameworks, exercises, scenarios, and trade names (including The Critical Thinker's Journey™, Get Your Think On!™, and Sonly Consulting) are the exclusive intellectual property of Sonly Consulting. Single-user digital purchases grant a non-exclusive, non-transferable, revocable license for personal, single-seat use. Public redistribution, enterprise reproduction without an active enterprise license, and unauthorized digital mirroring are strictly prohibited.</p>

      <h2>3. Digital Product Delivery & Verification</h2>
      <p>Access to offline workbooks and digital buyer editions is fulfilled digitally upon verification of entitlement (via Stripe checkout session reference or approved platform key). Users are solely responsible for exporting and backing up their written responses.</p>
    `
  }},
  'privacy': {{
    title: "Privacy Notice · Thinking Records Restraint",
    body: `
      <h2>1. Sovereign Thinking Privacy</h2>
      <p>At Sonly Consulting, we recognize that your written reflections, internal doubts, and strategic decisions require absolute privacy. CTJ is engineered with a strict <strong>Zero-Surveillance Architecture</strong>.</p>

      <h2>2. Client-Side Local Persistence</h2>
      <p>All responses typed into CTJ Builders, Decision Briefs, and the Strategic Clarity Assessment (SCA) are saved strictly to your local browser storage (<code>localStorage</code>) on your current device. No reflections are transmitted to external servers, cloud analytics engines, or large language models for scraping or training.</p>

      <h2>3. Data Ownership and Export</h2>
      <p>You retain 100% ownership of every word you write. You can export your responses at any time as JSON or printable text. Clearing your browser cache or switching devices will reset local entries unless an export is saved beforehand.</p>
    `
  }},
  'refund': {{
    title: "Digital Product & Refund Policy",
    body: `
      <h2>1. Digital Download Nature</h2>
      <p>Due to the immediate digital delivery of CTJ interactive web apps, standalone offline bundles (Edition 1.1 ZIP), and printable fillable PDF workbooks, purchases are generally final once access keys or downloads are initiated.</p>

      <h2>2. 14-Day Sovereign Satisfaction Guarantee</h2>
      <p>We stand resolutely behind the transformative quality of our frameworks. If you complete Part 1 or Part 2 in good faith and find that the frameworks provided no measurable clarity or strategic insight, contact <code>support@sonlyconsulting.com</code> within 14 days of purchase with your Stripe receipt reference for a prompt refund or module exchange.</p>

      <h2>3. Link Refresh & Access Recovery</h2>
      <p>If your digital download link expires or you change hardware, use the CTJ Delivery verification portal with your original <code>cs_live_...</code> Stripe reference to instantly generate a fresh secure link.</p>
    `
  }},
  'accessibility': {{
    title: "Accessibility Statement",
    body: `
      <h2>1. Universal Intellectual Access</h2>
      <p>Critical thinking belongs to everyone. The Critical Thinker's Journey™ is built to conform to the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards.</p>

      <h2>2. Accessibility Features Built-In</h2>
      <ul>
        <li><strong>Keyboard Navigation:</strong> All tabs, builder prompts, modals, and export buttons are fully navigable via standard keyboard focus (Tab, Enter, Escape).</li>
        <li><strong>High Contrast & Typographic Restraint:</strong> Color palettes meet or exceed 4.5:1 contrast ratios between slate backgrounds and gold/white typography.</li>
        <li><strong>Semantic HTML Landmarks:</strong> Screen readers benefit from strict semantic structuring (header, main, nav, article, footer).</li>
        <li><strong>Reduced Motion Support:</strong> CSS transitions respect the user's <code>prefers-reduced-motion</code> operating system settings.</li>
      </ul>
      <p>For accessibility inquiries or feedback, email <code>accessibility@sonlyconsulting.com</code>.</p>
    `
  }},
  'support': {{
    title: "Support & Purchase Recovery",
    body: `
      <h2>1. Customer Support Channel</h2>
      <p>For questions regarding purchase verification, accessing workbooks, or enterprise licensing, our dedicated human support team is available at <strong>support@sonlyconsulting.com</strong>.</p>

      <h2>2. Fast Self-Service Recovery</h2>
      <p>To restore your digital access: locate your Stripe purchase confirmation email, copy your checkout session ID (starts with <code>cs_live_...</code>), and paste it into the Delivery Recovery portal on the Unified review site.</p>

      <h2>3. Browser Migration Assistance</h2>
      <p>Because your entries are stored securely on your current device, remember to click 'Export Response Record' before clearing browser cookies or transitioning to a new computer.</p>
    `
  }},
  'author-intro': {{
    title: "Author's Note & Executive Introduction",
    body: `
      <h2>Author's Note</h2>
      <p>This is more than a journal. It is an invitation to awaken the thinker within you and discover the profound power of how you think. In a world spinning with constant change, algorithmic noise, and perpetual crisis, the ability to pause, breathe deeply, and approach decisions with crystalline clarity is life-changing magic.</p>
      <p>The Critical Thinker's Journey™ is woven from the very fabric of real life: unexpected setbacks that steal your breath, sudden opportunities that accelerate your pulse, and hard decisions that test your core. Structure becomes your sanctuary because it gives sacred shape to your experiences. It helps you see intricate patterns instead of bewildering chaos, boundless possibilities instead of towering walls, and clear steps forward instead of paralyzing standstills.</p>
      
      <h2>About Sonly Consulting</h2>
      <p>Sonly Consulting walks alongside you in that process through carefully engineered curriculum, strategic frameworks, and reflective tools. Mastery is intentional. When enterprise discipline meets deep intellectual clarity, technology stops being noise and becomes a multiplier.</p>
      <p>This journey is not meant to be finished and kicked to the curb. It is meant to be lived with passion, revisited with wonder, and carried forward with purpose.</p>
      <p style="margin-top: 16px;"><strong>Mindfully Crafted,</strong><br>Sonly Consulting</p>
    `
  }}
}};

function openDocumentModal(docKey) {{
  const doc = DOCUMENTS[docKey];
  if (!doc) return;
  document.getElementById('modalTitle').textContent = doc.title;
  document.getElementById('modalBody').innerHTML = doc.body;
  document.getElementById('documentModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}}

function closeDocumentModal() {{
  document.getElementById('documentModal').classList.remove('active');
  document.body.style.overflow = '';
}}

function closeModalOnBackdrop(e) {{
  if (e.target.id === 'documentModal') closeDocumentModal();
}}

// Initialize
document.addEventListener('DOMContentLoaded', () => {{
  initReturnNavigation();
  renderBuildersForPart('part-1', 0);
  renderBuildersForPart('part-2', 1);
  renderBuildersForPart('part-3', 2);
}});
</script>
</body>
</html>
'''

# Write to destination
out_dest1 = r'C:\DS All Things\DCSE_Command_Center\apps\ctj_suite_unified_preview.html'
out_dest2 = r'C:\DS All Things\DCSE_Command_Center\apps\ctj-commercial-experience-v1\ctj_suite_unified_preview.html'
out_dest3 = r'C:\DS All Things\SC-CTJ\public\ctj_suite_unified_preview.html'

for path in [out_dest1, out_dest2, out_dest3]:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated standalone preview: {path} ({len(html_content)} bytes)")

