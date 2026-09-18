import type { Settings } from "../lib/types";

export type SfxName =
  | "select"
  | "place"
  | "invalid"
  | "rotate"
  | "connect"
  | "activate"
  | "reset"
  | "hint"
  | "discover"
  | "complete"
  | "unlock"
  | "rule_change"
  | "achievement"
  | "final";

const SFX_FILES: Record<SfxName, string> = {
  select: "sfx_select",
  place: "sfx_place",
  invalid: "sfx_invalid",
  rotate: "sfx_rotate",
  connect: "sfx_connect",
  activate: "sfx_activate",
  reset: "sfx_reset",
  hint: "sfx_hint",
  discover: "sfx_discover",
  complete: "sfx_complete",
  unlock: "sfx_unlock",
  rule_change: "sfx_rule_change",
  achievement: "sfx_achievement",
  final: "sfx_final",
};

const AUDIO_DIR = "/media/audio/";

export interface SceneAudio {
  music: string | null;
  ambience: string | null;
}

/**
 * Central audio engine. Music, ambience, and SFX run on separate channels
 * with independent volumes. Nothing plays before a user gesture: ensure()
 * must be called from a gesture handler before any playback.
 */
class AudioEngine {
  private inited = false;
  private musicEls: HTMLAudioElement[] = [];
  private activeMusic = 0;
  private ambEl: HTMLAudioElement | null = null;
  private sfxPool: HTMLAudioElement[] = [];
  private sfxIndex = 0;
  private settings: Settings | null = null;
  private currentMusic: string | null = null;
  private currentAmbience: string | null = null;
  private fadeTimer: number | null = null;
  private suspended = false;
  private hiddenPausedMusic = new Set<number>();
  private hiddenPausedAmbience = false;

  ensure(): void {
    if (this.inited) return;
    this.inited = true;
    for (let i = 0; i < 2; i++) {
      const el = new Audio();
      el.loop = true;
      el.preload = "auto";
      this.musicEls.push(el);
    }
    this.ambEl = new Audio();
    this.ambEl.loop = true;
    for (let i = 0; i < 10; i++) {
      const el = new Audio();
      el.preload = "auto";
      this.sfxPool.push(el);
    }
    if (document.hidden) this.suspended = true;
    document.addEventListener("visibilitychange", () => {
      this.duck(document.hidden);
    });
    (window as unknown as Record<string, unknown>).__MI_AUDIO_DEBUG__ = () => ({
      inited: this.inited,
      suspended: this.suspended,
      hiddenPausedMusic: [...this.hiddenPausedMusic],
      hiddenPausedAmbience: this.hiddenPausedAmbience,
      musicPaused: this.musicEls.map((e) => e.paused),
      ambPaused: this.ambEl ? this.ambEl.paused : true,
    });
  }

  /** Pauses when the tab hides and restores exactly what was playing on return. */
  private duck(hidden: boolean): void {
    if (!this.inited) return;
    if (hidden) {
      this.hiddenPausedMusic.clear();
      this.musicEls.forEach((el, index) => {
        if (!el.paused) {
          el.pause();
          this.hiddenPausedMusic.add(index);
        }
      });
      this.hiddenPausedAmbience = Boolean(this.ambEl && !this.ambEl.paused);
      if (this.hiddenPausedAmbience && this.ambEl) {
        this.ambEl.pause();
      }
      return;
    }
    if (this.hiddenPausedMusic.size === 0 && !this.hiddenPausedAmbience) return;
    const s = this.settings;
    if (s && !s.muted && !this.suspended) {
      for (const index of this.hiddenPausedMusic) {
        const el = this.musicEls[index];
        if (el?.src) el.play().catch(() => undefined);
      }
      if (this.hiddenPausedAmbience && this.ambEl?.src) {
        this.ambEl.play().catch(() => undefined);
      }
    }
    this.hiddenPausedMusic.clear();
    this.hiddenPausedAmbience = false;
  }

  applySettings(s: Settings): void {
    this.settings = s;
    if (!this.inited) return;
    const m = s.muted ? 0 : s.masterVolume;
    if (this.ambEl) this.ambEl.volume = Math.min(1, m * s.ambienceVolume * 0.9);
    for (const el of this.musicEls) el.volume = Math.min(1, m * s.musicVolume * 0.9);
    if (s.muted) {
      this.stopAllLoops();
    } else if (this.suspended === false) {
      // restore loops for the current scene if they were stopped by mute
      if (this.currentMusic) this.playMusic(this.currentMusic);
      if (this.currentAmbience && this.ambEl?.paused) {
        this.ambEl.play().catch(() => undefined);
      }
    }
  }

  private stopAllLoops(): void {
    for (const el of this.musicEls) el.pause();
    this.ambEl?.pause();
  }

  /** Crossfades to the given scene. Pass nulls to silence a channel. */
  setScene(scene: SceneAudio): void {
    if (!this.inited) return;
    if (scene.music !== this.currentMusic) {
      this.currentMusic = scene.music;
      if (scene.music) this.playMusic(scene.music);
      else this.fadeOutMusic();
    }
    if (scene.ambience !== this.currentAmbience) {
      this.currentAmbience = scene.ambience;
      if (!this.ambEl) return;
      if (scene.ambience) {
        const src = AUDIO_DIR + scene.ambience + ".ogg";
        if (!this.ambEl.src.endsWith(src)) {
          this.ambEl.src = src;
        }
        if (this.settings && !this.settings.muted && !this.suspended) {
          this.ambEl.play().catch(() => undefined);
        }
      } else {
        this.ambEl.pause();
      }
    }
  }

  private playMusic(name: string): void {
    const s = this.settings;
    if (!s || s.muted) return;
    const src = AUDIO_DIR + name + ".ogg";
    const incoming = this.musicEls[1 - this.activeMusic];
    const outgoing = this.musicEls[this.activeMusic];
    if (incoming.dataset.name === name && !incoming.paused) return;
    incoming.dataset.name = name;
    incoming.src = src;
    incoming.volume = 0;
    incoming.currentTime = 0;
    incoming
      .play()
      .then(() => this.fade([incoming, 0, this.musicVol()], [outgoing, this.musicVol(), 0], 900))
      .catch(() => {
        // File missing or codec unsupported. Music is optional ambience.
      });
    this.activeMusic = 1 - this.activeMusic;
  }

  private musicVol(): number {
    const s = this.settings;
    if (!s || s.muted) return 0;
    return Math.min(1, s.masterVolume * s.musicVolume * 0.9);
  }

  private fadeOutMusic(): void {
    const outgoing = this.musicEls[this.activeMusic];
    this.fade(null, [outgoing, outgoing.volume, 0], 600);
  }

  private fade(
    fadeIn: [HTMLAudioElement, number, number] | null,
    fadeOut: [HTMLAudioElement, number, number] | null,
    ms: number
  ): void {
    if (this.fadeTimer) window.clearInterval(this.fadeTimer);
    const start = performance.now();
    const tick = () => {
      const t = Math.min(1, (performance.now() - start) / ms);
      if (fadeIn) {
        fadeIn[0].volume = fadeIn[1] + (fadeIn[2] - fadeIn[1]) * t;
      }
      if (fadeOut) {
        fadeOut[0].volume = Math.max(0, fadeOut[1] + (fadeOut[2] - fadeOut[1]) * t);
        if (t >= 1) fadeOut[0].pause();
      }
      if (t >= 1 && this.fadeTimer) {
        window.clearInterval(this.fadeTimer);
        this.fadeTimer = null;
      }
    };
    this.fadeTimer = window.setInterval(tick, 50);
    tick();
  }

  playSfx(name: SfxName): void {
    if (!this.inited || !this.settings || this.settings.muted || this.suspended) return;
    const s = this.settings;
    const el = this.sfxPool[this.sfxIndex];
    this.sfxIndex = (this.sfxIndex + 1) % this.sfxPool.length;
    el.src = AUDIO_DIR + SFX_FILES[name] + ".ogg";
    el.volume = Math.min(1, s.masterVolume * s.sfxVolume);
    el.currentTime = 0;
    el.play().catch(() => undefined);
  }

  /** One-shot completion cue. */
  playCompletionCue(): void {
    if (!this.inited || !this.settings || this.settings.muted) return;
    const el = new Audio(AUDIO_DIR + "music_complete.ogg");
    el.volume = Math.min(1, this.settings.masterVolume * this.settings.musicVolume);
    el.play().catch(() => undefined);
  }

  /** Suspends everything (pause overlay, leaving the game). */
  suspend(): void {
    this.suspended = true;
    this.stopAllLoops();
  }

  resume(): void {
    this.suspended = false;
    if (!this.settings || this.settings.muted) return;
    if (this.currentMusic) this.playMusic(this.currentMusic);
    if (this.currentAmbience && this.ambEl) this.ambEl.play().catch(() => undefined);
  }
}

export const audio = new AudioEngine();
