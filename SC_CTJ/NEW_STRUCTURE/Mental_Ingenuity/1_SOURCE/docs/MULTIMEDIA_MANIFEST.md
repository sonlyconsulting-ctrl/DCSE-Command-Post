# Multimedia Manifest

Every asset below is original. Raster artwork was generated for this product,
then converted to WebP. The cinematic was rendered programmatically frame by
frame and encoded locally. All audio was synthesized programmatically from
periodic components so loops join seamlessly. Provenance: created during this
build. License status: original work commissioned for Mental Ingenuity.

Sizes in bytes as delivered.

## Raster images

| ID | File | Purpose | View | Method | Format | Dims | Size | Accessibility | Verified |
|---|---|---|---|---|---|---|---|---|---|
| IMG-HERO | img/hero.webp | Opening environment | Start | Generated art, WebP convert | WebP | approx 1344x768 | 146932 | Decorative, aria hidden | HTTP 200, shown |
| IMG-MAP | img/map.webp | Ascent vista | Chamber map | Generated art | WebP | approx 1344x768 | 178010 | Decorative, aria hidden | HTTP 200, shown |
| IMG-SIG | img/chamber_signal.webp | Chamber identity | Signal Chamber | Generated art | WebP | approx 1344x768 | 146396 | Decorative backdrop | HTTP 200 |
| IMG-FRG | img/chamber_forge.webp | Chamber identity | Constraint Forge | Generated art | WebP | approx 1344x768 | 123912 | Decorative backdrop | HTTP 200 |
| IMG-PRS | img/chamber_perspective.webp | Chamber identity | Perspective Engine | Generated art | WebP | approx 1344x768 | 95198 | Decorative backdrop | HTTP 200 |
| IMG-CSL | img/chamber_causal.webp | Chamber identity | Causal Labyrinth | Generated art | WebP | approx 1344x768 | 184992 | Decorative backdrop | HTTP 200 |
| IMG-VLT | img/chamber_vault.webp | Chamber identity | Paradox Vault | Generated art | WebP | approx 1344x768 | 97640 | Decorative backdrop | HTTP 200 |
| IMG-SUM | img/chamber_summit.webp | Chamber identity | The Summit | Generated art | WebP | approx 1344x768 | 133636 | Decorative backdrop | HTTP 200 |
| IMG-ABT | img/about.webp | About monument | About | Generated art | WebP | approx 1024x1024 | 38842 | Descriptive alt text | HTTP 200 |
| IMG-SOC | img/social.webp | Promotional preview | og meta | Generated art | WebP | approx 1344x768 | 130140 | Meta only | HTTP 200 |
| IMG-PST | video/poster.jpg | Video poster and fallback | Cinematic | Rendered frame from video | JPEG | 1920x1080 | 120583 | Alt text on fallback img | HTTP 200 |

## Vector and programmatic graphics

| ID | File | Purpose | Method | Accessibility |
|---|---|---|---|---|
| VEC-FAV | favicon.svg | Application icon | Hand written SVG | aria label on emblem |
| VEC-EML | Emblem component | Signature and achievement emblems | Inline SVG in ui.tsx | Role img with title label |
| VEC-SIG | Signal, forge, perspective, summit boards | Puzzle surfaces | Programmatic SVG and CSS | Groups carry labels and focus |

## Video

| ID | File | Purpose | Method | Format | Codec | Dims | fps | Duration | Size | Loop | Accessibility | Verified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VID-MP4 | video/opening.mp4 | Opening cinematic | Programmatic render, scripts/make_video.py | MP4 | H.264 High, yuv420p | 1920x1080 | 24 | 16s | 1466938 | No | Poster, captions, transcript, skip, replay, reduced motion still | Plays muted in Chromium |
| VID-WEBM | video/opening.webm | Web fallback | Same frames | WebM | VP9 | 1920x1080 | 24 | 16s | 3009859 | No | Same | Served 200 |

No text is rendered inside video frames. Brand text overlays in HTML only.

## Music

All music loops are OGG Vorbis, mono, 44.1 kHz, seamless by construction.

| ID | File | Purpose | Duration | Size | Loop | Verified |
|---|---|---|---|---|---|---|
| MUS-OPN | audio/music_opening.ogg | Opening theme | 32s | 232856 | Yes | Decodes |
| MUS-MAP | audio/music_map.ogg | Chamber map loop | 40s | 303944 | Yes | Decodes |
| MUS-FOC | audio/music_focus.ogg | Focus loop: Signal, Causal | 36s | 252976 | Yes | Decodes |
| MUS-STR | audio/music_structure.ogg | Structure loop: Forge, Perspective | 36s | 272167 | Yes | Decodes |
| MUS-TEN | audio/music_tension.ogg | Tension loop: Paradox | 36s | 274785 | Yes | Decodes |
| MUS-SUM | audio/music_summit.ogg | Summit challenge track | 40s | 294363 | Yes | Decodes |
| MUS-CMP | audio/music_complete.ogg | Completion and signature cue | 12s | 16731 | No | Decodes |

## Ambience

| ID | File | Chamber | Duration | Size | Loop | Verified |
|---|---|---|---|---|---|---|
| AMB-SIG | audio/amb_signal.ogg | Signal | 28s | 223623 | Yes | Decodes |
| AMB-FRG | audio/amb_forge.ogg | Forge | 28s | 223937 | Yes | Decodes |
| AMB-PRS | audio/amb_perspective.ogg | Perspective | 28s | 218485 | Yes | Decodes |
| AMB-CSL | audio/amb_causal.ogg | Causal | 28s | 217188 | Yes | Decodes |
| AMB-VLT | audio/amb_vault.ogg | Paradox | 28s | 226194 | Yes | Decodes |
| AMB-SUM | audio/amb_summit.ogg | Summit and signature | 28s | 214324 | Yes | Decodes |

## Sound effects

| ID | File | Function | Duration | Size |
|---|---|---|---|---|
| SFX-SEL | sfx_select.ogg | Selection confirm | 0.2s | 3885 |
| SFX-PLC | sfx_place.ogg | Valid placement | 0.3s | 4049 |
| SFX-INV | sfx_invalid.ogg | Invalid action | 0.3s | 6485 |
| SFX-ROT | sfx_rotate.ogg | Rotation | 0.3s | 3918 |
| SFX-CNN | sfx_connect.ogg | Node or signal connection | 0.3s | 4121 |
| SFX-ACT | sfx_activate.ogg | Energy activation | 0.5s | 4375 |
| SFX-RST | sfx_reset.ogg | Reset | 0.4s | 4266 |
| SFX-HNT | sfx_hint.ogg | Hint activation | 0.6s | 4537 |
| SFX-DSC | sfx_discover.ogg | Evidence discovery | 0.7s | 4652 |
| SFX-CMP | sfx_complete.ogg | Chamber completion | 1.2s | 6103 |
| SFX-UNL | sfx_unlock.ogg | Chamber unlock | 0.8s | 5256 |
| SFX-LAW | sfx_rule_change.ogg | Rule change signal | 1.0s | 5140 |
| SFX-ACH | sfx_achievement.ogg | Achievement earned | 0.9s | 5005 |
| SFX-FIN | sfx_final.ogg | Final ascent completion | 2.6s | 8867 |

Every SFX also has visible feedback: cell locks, mirror turns, chips, pulses,
toasts, or the law panel revision.

## Caption and transcript content

The cinematic carries captions on demand and a full transcript in the reduced
motion alternative:

1. 0 to 3s: Near darkness. An immense obsidian chamber waits.
2. 3 to 7s: Gold pathways wake across the stone, carrying emerald light.
3. 7 to 11s: Silver rings turn slowly, searching for alignment.
4. 11 to 16s: Monoliths rise. The gate of the Ingenuity Ascent stands open.

There is no spoken dialogue, so no narrator voice was created or cloned.

## Integration map

- Cinematic view: VID-MP4 plus VID-WEBM, IMG-PST, captions, skip, replay
- Start: IMG-HERO, MUS-OPN
- Map: IMG-MAP, MUS-MAP
- Signal: IMG-SIG, MUS-FOC, AMB-SIG, SFX-CNN, SFX-PLC, SFX-INV, SFX-HNT, SFX-CMP
- Forge: IMG-FRG, MUS-STR, AMB-FRG, SFX-ROT, SFX-ACT, SFX-UNL, SFX-RST
- Perspective: IMG-PRS, MUS-STR, AMB-PRS, SFX-ROT, SFX-HNT
- Causal: IMG-CSL, MUS-FOC, AMB-CSL, SFX-SEL, SFX-CNN, SFX-ACT
- Paradox: IMG-VLT, MUS-TEN, AMB-VLT, SFX-SEL, SFX-DSC, SFX-INV
- Summit: IMG-SUM, MUS-SUM, AMB-SUM, SFX-LAW on revision, SFX-FIN on completion
- Record and Signature: MUS-CMP cue, SFX-ACH on achievements
- UI chrome: SFX-SEL on menu selection

## Performance report

- Startup payload: JS 76.9 kB gzipped, CSS 4.9 kB gzipped, plus favicon
- Chamber art lazy loads and hides gracefully on failure
- Video poster prevents layout shift. Loading indicator shown until canplay
- Music and ambience preload on demand per scene, not all at startup
- Total media footprint approx 9.2 MB, dominated by the WebM fallback which
  browsers skip when MP4 is supported

## QA report summary

Playback, skip, replay, failure fallback, captions, reduced motion still,
muted autoplay rule, per channel volumes, mute persistence, tab hide ducking,
pause suspension, and stacked navigation were all exercised in tests/media.mjs
and tests/e2e.mjs with 46 of 46 and 44 of 44 passing respectively.
