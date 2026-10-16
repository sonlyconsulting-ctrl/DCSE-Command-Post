import os
import re
import shutil

src_path = 'apps/escd/web/scripture.html'
with open(src_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Custom styles for Sasser Hill Cover & Dual City branding
sasser_css = """
/* === SASSER HILL / DALLAS & ATLANTA TEXAS THEME EXTENSIONS === */
:root {
  --cowboys-navy: #041E42;
  --cowboys-silver: #869397;
  --cowboys-light-silver: #D1D5DB;
  --cowboys-blue: #003594;
  --atlanta-pine: #1C3D2B;
  --atlanta-forest: #2D5A3E;
  --texas-gold: #C9A55A;
  --texas-warm-gold: #E5C158;
}

.sasser-cover {
  max-width: 920px;
  margin: 0 auto;
  padding: 10px 0 40px;
}

.two-cities-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.city-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 9999px;
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.city-pill:hover {
  transform: translateY(-2px);
}

.city-pill.dallas {
  background: linear-gradient(135deg, rgba(4, 30, 66, 0.95), rgba(0, 53, 148, 0.85));
  border: 1px solid rgba(134, 147, 151, 0.6);
  color: #F3F4F6;
  box-shadow: 0 4px 14px rgba(0, 53, 148, 0.3);
}

.city-pill.atlanta {
  background: linear-gradient(135deg, rgba(28, 61, 43, 0.95), rgba(45, 90, 62, 0.85));
  border: 1px solid rgba(201, 165, 90, 0.6);
  color: #F5EEDB;
  box-shadow: 0 4px 14px rgba(28, 61, 43, 0.3);
}

.city-meta {
  font-size: 0.7rem;
  opacity: 0.8;
  font-weight: 400;
}

.bridge-divider {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--texas-gold);
}

.bridge-line {
  width: 24px;
  height: 1px;
  background: var(--texas-gold);
  opacity: 0.5;
}

.bridge-star {
  font-size: 0.8rem;
  color: var(--texas-gold);
}

.cover-hero-card {
  background: linear-gradient(180deg, rgba(7, 20, 39, 0.92) 0%, rgba(4, 30, 66, 0.85) 100%);
  border: 1px solid rgba(201, 165, 90, 0.4);
  border-radius: 16px;
  padding: 36px 28px;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55);
  margin-bottom: 24px;
}

.cover-hero-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(201, 165, 90, 0.08) 0%, transparent 65%);
  pointer-events: none;
}

.lone-star-crest {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  color: var(--texas-gold);
  filter: drop-shadow(0 0 12px rgba(201, 165, 90, 0.45));
}

.star-svg {
  width: 100%;
  height: 100%;
}

.edition-label {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 9999px;
  background: rgba(201, 165, 90, 0.15);
  border: 1px solid var(--texas-gold);
  color: var(--texas-gold);
  font-family: 'Inter', sans-serif;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 14px;
}

.cover-title {
  font-family: 'EB Garamond', Georgia, serif;
  font-size: 2.85rem;
  font-weight: 500;
  color: #F8F9FA;
  letter-spacing: -0.02em;
  margin: 0 0 8px;
  line-height: 1.15;
}

.cover-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--texas-gold);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin: 0 0 18px;
}

.cover-creed {
  max-width: 680px;
  margin: 0 auto 28px;
  font-family: 'Lora', Georgia, serif;
  font-size: 0.98rem;
  color: #D1D5DB;
  line-height: 1.68;
}

.cover-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}

.cover-btn-enter {
  padding: 13px 28px;
  font-size: 0.92rem;
  letter-spacing: 0.04em;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 6px 20px rgba(201, 165, 90, 0.35);
}

.cover-btn-ambiance {
  padding: 13px 24px;
  font-size: 0.9rem;
  border-radius: 8px;
  border-color: rgba(201, 165, 90, 0.5);
  color: var(--texas-gold);
}

.cover-btn-ambiance:hover {
  background: rgba(201, 165, 90, 0.12);
  border-color: var(--texas-gold);
}

.dedication-card {
  background: rgba(10, 25, 47, 0.7);
  border: 1px solid rgba(134, 147, 151, 0.3);
  border-left: 4px solid var(--texas-gold);
  border-radius: 10px;
  padding: 18px 22px;
  margin-bottom: 24px;
  font-family: 'Inter', sans-serif;
}

.dedication-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}

.dedication-tag {
  color: var(--texas-gold);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.dedication-loc {
  color: #9CA3AF;
  font-size: 0.72rem;
}

.dedication-body {
  font-family: 'Lora', Georgia, serif;
  font-style: italic;
  font-size: 0.88rem;
  color: #E5E7EB;
  line-height: 1.6;
}

.portal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-bottom: 24px;
}

@media (max-width: 700px) {
  .portal-grid { grid-template-columns: 1fr; }
  .cover-title { font-size: 2.15rem; }
}

.portal-card {
  border-radius: 12px;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.portal-card:hover {
  transform: translateY(-3px);
}

.portal-card.dallas-card {
  background: linear-gradient(160deg, #041E42 0%, #071931 100%);
  border: 1px solid rgba(134, 147, 151, 0.5);
  box-shadow: 0 8px 24px rgba(4, 30, 66, 0.4);
}

.portal-card.atlanta-card {
  background: linear-gradient(160deg, #1C3D2B 0%, #0F2318 100%);
  border: 1px solid rgba(201, 165, 90, 0.45);
  box-shadow: 0 8px 24px rgba(28, 61, 43, 0.4);
}

.portal-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.portal-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  flex-shrink: 0;
}

.portal-icon-box.cowboys {
  background: rgba(0, 53, 148, 0.4);
  border: 1px solid #869397;
  color: #FFFFFF;
}

.portal-icon-box.piney {
  background: rgba(45, 90, 62, 0.5);
  border: 1px solid var(--texas-gold);
  color: var(--texas-gold);
}

.portal-eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--texas-gold);
}

.portal-title {
  margin: 2px 0 0;
  font-family: 'EB Garamond', Georgia, serif;
  font-size: 1.35rem;
  color: #FFFFFF;
}

.portal-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #D1D5DB;
  line-height: 1.55;
  margin: 0 0 16px;
}

.portal-features {
  display: grid;
  gap: 6px;
  margin-bottom: 20px;
  font-family: 'Inter', sans-serif;
  font-size: 0.76rem;
  color: #E5E7EB;
}

.btn-cowboys {
  background: #003594;
  color: #FFFFFF;
  border: 1px solid #869397;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.82rem;
  width: 100%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.btn-cowboys:hover {
  background: #041E42;
  border-color: #FFFFFF;
}

.capabilities-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.cap-item {
  background: rgba(7, 20, 39, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 14px;
  cursor: pointer;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.cap-item:hover {
  border-color: var(--texas-gold);
  transform: translateY(-2px);
}

.cap-icon {
  font-size: 1.25rem;
  margin-bottom: 6px;
}

.cap-title {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  color: #F3F4F6;
  margin-bottom: 4px;
}

.cap-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  color: #9CA3AF;
  line-height: 1.4;
}

.sasser-tag-pill {
  background: rgba(0, 53, 148, 0.3);
  border: 1px solid #869397;
  color: #F3F4F6;
  border-radius: 4px;
  padding: 2px 7px;
  font-size: 0.68rem;
  font-weight: 600;
}
"""

# Inject sasser_css right before </style>
content = content.replace('</style>', sasser_css + '\n</style>')

# Replace App Title in header
header_find = '<div class="app-logo"><span>✦</span> Sacred Study</div>'
header_replace = '<div class="app-logo" style="display:flex;align-items:center;gap:8px;"><span style="color:var(--texas-gold)">✦</span><span>Religious &amp; Worldly Studies</span><span class="sasser-tag-pill">Sasser Hill Edition</span></div>'
content = content.replace(header_find, header_replace)

# Add Cover Tab Button as the first button in tab-nav
nav_find = '<nav class="tab-nav" role="tablist">'
nav_replace = """<nav class="tab-nav" role="tablist">
  <button class="tab-btn active" role="tab" onclick="switchTab('cover')">✦ Sasser Hill Home</button>"""
content = content.replace(nav_find, nav_replace)

# Remove active class from pane-daily and tab-btn daily
content = content.replace("<button class=\"tab-btn active\" role=\"tab\" onclick=\"switchTab('daily')\">", "<button class=\"tab-btn\" role=\"tab\" onclick=\"switchTab('daily')\">")
content = content.replace('<section class="tab-pane active" id="pane-daily"', '<section class="tab-pane" id="pane-daily"')

# Cover pane HTML
cover_html = """
<section class="tab-pane active" id="pane-cover" role="tabpanel">
  <div class="sasser-cover">
    
    <!-- Top Two Cities Banner -->
    <div class="two-cities-badge">
      <div class="city-pill dallas">
        <span class="city-icon">⭐</span>
        <span class="city-name">DALLAS, TX</span>
        <span class="city-meta">32.7767° N · Cowboys Nation</span>
      </div>
      <div class="bridge-divider">
        <span class="bridge-line"></span>
        <span class="bridge-star">✦</span>
        <span class="bridge-line"></span>
      </div>
      <div class="city-pill atlanta">
        <span class="city-icon">🌲</span>
        <span class="city-name">ATLANTA, TX</span>
        <span class="city-meta">33.1137° N · Sasser Hill</span>
      </div>
    </div>

    <!-- Hero Title Box -->
    <div class="cover-hero-card">
      <div class="lone-star-crest">
        <svg class="star-svg" viewBox="0 0 100 100" fill="currentColor">
          <polygon points="50,5 64,36 98,36 70,57 81,91 50,70 19,91 30,57 2,36 36,36"/>
        </svg>
      </div>
      <div class="edition-label">SPECIAL COMMISSION EDITION · TESTER RELEASE</div>
      <h1 class="cover-title">Religious and Worldly Studies</h1>
      <div class="cover-subtitle">Custom Made for Sasser Hill</div>
      <p class="cover-creed">
        From the pine-canopied hills of East Texas to the Lone Star gridiron of Dallas, faith and discipline walk hand-in-hand. 
        Timeless biblical covenants, original languages, and practical wisdom for leadership on and off the field.
      </p>
      
      <!-- Primary Action Buttons -->
      <div class="cover-actions">
        <button class="btn btn-primary cover-btn-enter" onclick="switchTab('reader')">
          <span>📖 Enter The Study &amp; Reader</span>
          <span class="btn-arrow">→</span>
        </button>
        <button class="btn btn-ghost cover-btn-ambiance" id="coverAmbianceBtn" onclick="toggleAmbiance()">
          <span id="coverAmbianceIcon">🎵</span>
          <span id="coverAmbianceLabel">Play Scriptorium Ambiance</span>
        </button>
      </div>
    </div>

    <!-- Dedication Card -->
    <div class="dedication-card">
      <div class="dedication-header">
        <span class="dedication-tag">SASSER HILL TESTER DEDICATION</span>
        <span class="dedication-loc">Atlanta, Texas · Cass County</span>
      </div>
      <div class="dedication-body">
        “This customized edition is prepared with deep respect for the testers and family at Sasser Hill in Atlanta, Texas, 
        and our fellow Dallas Cowboys faithful across the Lone Star State. Whether opening 2 Samuel 7 for contemplative stillness 
        or seeking biblical stamina before Sunday kickoff, this interactive study is built to strengthen your inner foundation.”
      </div>
    </div>

    <!-- The Two Cities Portal Grid -->
    <div class="portal-grid">
      
      <!-- Dallas Card -->
      <div class="portal-card dallas-card">
        <div class="portal-header">
          <div class="portal-icon-box cowboys">⭐</div>
          <div>
            <div class="portal-eyebrow">DALLAS, TEXAS · GRIDIRON &amp; DRIVE</div>
            <h3 class="portal-title">Game Day Focus &amp; Endurance</h3>
          </div>
        </div>
        <p class="portal-desc">
          Focus, brotherhood, and perseverance under the lights. Scripture forged for warriors of faith and athletic discipline.
        </p>
        <div class="portal-features">
          <div class="p-feature">✓ <strong>Romans 8:</strong> More than conquerors in all trials</div>
          <div class="p-feature">✓ <strong>1 Corinthians 9:</strong> Run in such a way as to finish and win</div>
          <div class="p-feature">✓ <strong>Joshua 1:9:</strong> Be strong and courageous; do not be afraid</div>
        </div>
        <button class="btn btn-cowboys" onclick="openGameDayDevotional()">
          ⭐ Load Dallas Cowboys Focus (Romans 8)
        </button>
      </div>

      <!-- Atlanta Card -->
      <div class="portal-card atlanta-card">
        <div class="portal-header">
          <div class="portal-icon-box piney">🌲</div>
          <div>
            <div class="portal-eyebrow">ATLANTA, TEXAS · PINEY WOODS</div>
            <h3 class="portal-title">Sasser Hill Heritage &amp; Stillness</h3>
          </div>
        </div>
        <p class="portal-desc">
          Rooted like tall East Texas pines. Covenant promises, family devotion, and quiet reflection in the heart of Cass County.
        </p>
        <div class="portal-features">
          <div class="p-feature">✓ <strong>2 Samuel 7:</strong> David's covenant (All 29 verses complete)</div>
          <div class="p-feature">✓ <strong>Psalm 139:</strong> Searched, known, and guided in the deep woods</div>
          <div class="p-feature">✓ <strong>Proverbs 3:5-6:</strong> Trust in the Lord with all your heart</div>
        </div>
        <button class="btn btn-sage" onclick="openAtlantaDevotional()">
          🌲 Load Atlanta Devotional (2 Samuel 7)
        </button>
      </div>

    </div>

    <!-- Studio Capabilities Preview -->
    <div class="capabilities-strip">
      <div class="cap-item" onclick="switchTab('reader')">
        <div class="cap-icon">🔊</div>
        <div class="cap-title">Whole Chapter Read Aloud</div>
        <div class="cap-desc">Continuous verse-by-verse reading with Male &amp; Female voice options.</div>
      </div>
      <div class="cap-item" onclick="toggleAmbiance()">
        <div class="cap-icon">🎵</div>
        <div class="cap-title">Scriptorium 432Hz Audio</div>
        <div class="cap-desc">Attached contemplative soundscape for focused prayer and study.</div>
      </div>
      <div class="cap-item" onclick="switchTab('daily')">
        <div class="cap-icon">🔍</div>
        <div class="cap-title">6-Layer Comparative Exegesis</div>
        <div class="cap-desc">Greek Koine, Hebrew Ivrit, Latin Vulgate, and leadership inquiries.</div>
      </div>
      <div class="cap-item" onclick="switchTab('reflection')">
        <div class="cap-icon">🎙️</div>
        <div class="cap-title">Voice Dictation Journal</div>
        <div class="cap-desc">Record your voice reading or dictate personal study notes.</div>
      </div>
    </div>

  </div>
</section>
"""

# Inject cover pane right after <main class="app-content">
main_find = '<main class="app-content">'
content = content.replace(main_find, main_find + '\n' + cover_html)

# Update switchTab implementation to handle 'cover' and update cover ambiance button
switch_find = """function switchTab(tab) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('pane-' + tab).classList.add('active');
  const tabs = ['daily', 'reader', 'reflection', 'history'];
  document.querySelectorAll('.tab-btn')[tabs.indexOf(tab)].classList.add('active');
"""
switch_replace = """function switchTab(tab) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  const targetPane = document.getElementById('pane-' + tab);
  if (targetPane) targetPane.classList.add('active');
  const tabs = ['cover', 'daily', 'reader', 'reflection', 'history'];
  const idx = tabs.indexOf(tab);
  if (idx !== -1 && document.querySelectorAll('.tab-btn')[idx]) {
    document.querySelectorAll('.tab-btn')[idx].classList.add('active');
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
"""
content = content.replace(switch_find, switch_replace)

# Add helper devotional loaders & cover ambiance button updates
helpers_js = """
function openGameDayDevotional() {
  S.book = 'Romans';
  S.chapter = 8;
  const bSel = document.getElementById('bookSelect');
  if (bSel) bSel.value = 'Romans';
  updateChapterSelect();
  const cSel = document.getElementById('chapterSelect');
  if (cSel) cSel.value = '8';
  switchTab('reader');
  loadChapter();
  toast('Loaded Dallas Cowboys Focus: Romans 8');
}

function openAtlantaDevotional() {
  S.book = '2 Samuel';
  S.chapter = 7;
  const bSel = document.getElementById('bookSelect');
  if (bSel) bSel.value = '2 Samuel';
  updateChapterSelect();
  const cSel = document.getElementById('chapterSelect');
  if (cSel) cSel.value = '7';
  switchTab('reader');
  loadChapter();
  toast('Loaded Sasser Hill Devotional: 2 Samuel 7 (All 29 Verses)');
}
"""
content = content.replace('function startAmbiance() {', helpers_js + '\nfunction startAmbiance() {')

# Synchronize coverAmbianceBtn state inside startAmbiance and stopAmbiance
content = content.replace("toast('Scriptorium contemplative ambiance track playing');", "toast('Scriptorium contemplative ambiance track playing'); const cLbl = document.getElementById('coverAmbianceLabel'); if (cLbl) cLbl.textContent = 'Pause Scriptorium Ambiance';")
content = content.replace("toast('Ambiance stopped');", "toast('Ambiance stopped'); const cLbl = document.getElementById('coverAmbianceLabel'); if (cLbl) cLbl.textContent = 'Play Scriptorium Ambiance';")

# Replace Title
content = re.sub(r'<title>.*?</title>', '<title>Religious and Worldly Studies — Custom Made for Sasser Hill</title>', content)

# Write output to apps/sc-sasser-hill/index.html
with open('apps/sc-sasser-hill/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully generated apps/sc-sasser-hill/index.html. Bytes:', len(content.encode('utf-8')))

# Now create zero-localhost standalone preview file sc_sasser_hill_preview.html with DCSE review bar
preview_bar = """
  <!-- DCSE Sovereign Executive Review Bar -->
  <div class="dcse-preview-bar" style="background:#041E42;border-bottom:1px solid #869397;padding:8px 16px;display:flex;align-items:center;justify-content:space-between;font-family:'Inter',sans-serif;font-size:0.75rem;color:#D1D5DB;z-index:9999;position:relative;">
    <div style="display:flex;align-items:center;gap:10px;">
      <span style="background:rgba(201,165,90,0.18);border:1px solid #C9A55A;color:#C9A55A;font-weight:700;font-size:0.65rem;letter-spacing:0.08em;padding:2px 8px;border-radius:4px;text-transform:uppercase;">SASSER HILL EDITION · ATLANTA &amp; DALLAS, TX</span>
      <strong style="color:#FFFFFF;font-weight:600;">Religious and Worldly Studies — Custom Made for Sasser Hill</strong>
    </div>
    <div style="display:flex;align-items:center;gap:14px;">
      <span>Target URL: <strong style="color:#C9A55A;">sc-sasser-hill.vercel.app</strong></span>
      <span style="color:#7EA898;font-weight:600;display:inline-flex;align-items:center;gap:5px;">● ZERO-LOCALHOST TESTER READY</span>
    </div>
  </div>
"""

preview_content = content.replace('<body>', '<body>\n' + preview_bar)
with open('sc_sasser_hill_preview.html', 'w', encoding='utf-8') as f:
    f.write(preview_content)

print('Successfully generated sc_sasser_hill_preview.html. Bytes:', len(preview_content.encode('utf-8')))
