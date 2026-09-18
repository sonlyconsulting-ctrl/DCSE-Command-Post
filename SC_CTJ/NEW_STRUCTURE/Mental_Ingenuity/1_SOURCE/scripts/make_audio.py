#!/usr/bin/env python3
"""Original music, ambience, and SFX synthesis for Mental Ingenuity.

All audio is generated programmatically (original programmatic assets).
Loop tracks are built from components whose periods divide the loop length,
so they loop seamlessly. Output: OGG Vorbis via ffmpeg.
"""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image  # noqa: F401  (ensures pillow present; not used here)

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100
OUT = os.path.join(os.path.dirname(__file__), "..", "public", "media", "audio")
os.makedirs(OUT, exist_ok=True)


def env_ad(t, a=0.01, d=None, sus=1.0, r=0.08):
    """ADSR-ish envelope."""
    n = len(t)
    e = np.ones(n)
    d = d if d is not None else max(0.01, t[-1] - r - 0.02)
    e[: max(1, int(a * SR))] = np.linspace(0, 1, max(1, int(a * SR)))
    rel_i = int((t[-1] - r) * SR)
    if rel_i < n:
        e[rel_i:] *= np.linspace(1, 0, n - rel_i)
    mid = slice(int(a * SR), max(int(a * SR), rel_i))
    e[mid] *= sus
    return e


def tone(freq, dur, shape="sine", amp=0.2, detune=0.0, pan=0.0):
    t = np.arange(int(dur * SR)) / SR
    f = freq * (1 + detune)
    if shape == "sine":
        w = np.sin(2 * np.pi * f * t)
    elif shape == "tri":
        w = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * f * t))
    elif shape == "square":
        w = np.sign(np.sin(2 * np.pi * f * t)) * 0.6
    else:  # saw soft
        w = (2 * (f * t % 1) - 1) * 0.5
    w *= env_ad(t, a=0.012, r=min(0.12, dur * 0.4))
    return w * amp


def place(buf, sig, at):
    i = int(at * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf) and j > i:
        buf[i:j] += sig[: j - i]


def note(buf, freq, at, dur, shape="sine", amp=0.2, detune=0.0, echo=0.0):
    place(buf, tone(freq, dur, shape, amp, detune), at)
    if echo > 0:
        place(buf, tone(freq, dur, shape, amp * echo, detune), at + 0.28)


def scale_freqs(root, steps):
    return [root * (2 ** (s / 12)) for s in steps]


def pad_loop(name, dur, root, steps, rhythm, noise_amt=0.0, tone_shape="sine",
             bass=True, sparkle=True, amp=0.16):
    """A loop-safe ambient music track.

    All pitched events use frequencies that are exact harmonics of 1/dur,
    guaranteeing a seamless loop.
    """
    rng = random.Random(hash(name) & 0xFFFF)
    buf = np.zeros(int(dur * SR))
    f0 = 1.0 / dur
    # Drone: two low harmonics, always periodic over dur.
    k_lo = max(2, int(round(root / f0)))
    t = np.arange(len(buf)) / SR
    drone = 0.5 * np.sin(2 * np.pi * k_lo * f0 * t) + 0.28 * np.sin(
        2 * np.pi * (k_lo * 1.5) * f0 * t
    )
    # slow amplitude LFO, periodic
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * (3 * f0) * t)
    buf += drone * lfo * amp * 0.55
    # Melodic events on a grid; each note envelope fits inside loop with margin.
    freqs = scale_freqs(root, steps)
    grid = dur / rhythm
    for i in range(rhythm):
        at = i * grid + rng.uniform(0, grid * 0.2)
        if rng.random() < 0.72:
            fq = rng.choice(freqs)
            # snap to harmonic of loop for perfect periodicity
            k = max(4, int(round(fq / f0)))
            fq = k * f0
            d = rng.uniform(0.8, min(2.2, grid * 1.6))
            if at + d > dur - 0.05:
                d = max(0.3, dur - 0.05 - at)
            note(buf, fq, at, d, tone_shape, amp=amp * rng.uniform(0.5, 1.0), echo=0.35)
    if bass:
        for i in range(0, rhythm, 4):
            k = k_lo // 2 if k_lo > 3 else k_lo
            note(buf, k * f0, i * grid, grid * 1.2, "sine", amp=amp * 0.8)
    if sparkle:
        for i in range(rhythm):
            if rng.random() < 0.16:
                k = int(round(rng.choice(freqs) * 2 / f0))
                at = i * grid + grid * 0.5
                d = 0.4
                if at + d < dur - 0.05:
                    note(buf, k * f0, at, d, "sine", amp=amp * 0.35)
    if noise_amt > 0:
        # loopable noise bed: generate then crossfade the wrap point
        n = len(buf)
        nz = rng.random() if False else np.random.default_rng(7).standard_normal(n)
        # simple lowpass via cumsum smoothing
        nz = np.convolve(nz, np.ones(120) / 120, mode="same")
        w = 1.0
        xfade = int(1.0 * SR)
        ramp = np.linspace(0, 1, xfade)
        nz[:xfade] = nz[:xfade] * ramp + nz[-xfade:] * (1 - ramp)
        nz /= max(1e-6, np.max(np.abs(nz)))
        buf += nz * noise_amt * amp
    buf /= max(1e-6, np.max(np.abs(buf)))
    buf *= 0.82
    write_ogg(name, buf)


def rng_seed(name):
    return random.Random(name)


def write_ogg(name, buf):
    buf16 = np.clip(buf, -1, 1)
    pcm = (buf16 * 32767).astype("<i2").tobytes()
    out = os.path.join(OUT, name + ".ogg")
    subprocess.run(
        [FFMPEG, "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
         "-c:a", "libvorbis", "-q:a", "3", out],
        input=pcm, check=True, capture_output=True,
    )
    print("wrote", out, os.path.getsize(out), "bytes")


def sfx(name, dur, build):
    buf = np.zeros(int(dur * SR))
    build(buf)
    buf /= max(1e-6, np.max(np.abs(buf)))
    buf *= 0.8
    write_ogg(name, buf)


def sweep(buf, f0, f1, at, dur, shape="sine", amp=0.5):
    t = np.arange(int(dur * SR)) / SR
    phase = 2 * np.pi * (f0 * t + (f1 - f0) * t * t / (2 * dur))
    w = np.sin(phase) if shape == "sine" else np.sign(np.sin(phase)) * 0.6
    w *= env_ad(t, a=0.008, r=min(0.1, dur * 0.5))
    place(buf, w * amp, at)


def main():
    # --- Music loops -------------------------------------------------------
    # opening theme: slowly awakening, gold and emerald
    pad_loop("music_opening", 32.0, 110.0, [0, 3, 7, 10, 12, 15], 16,
             noise_amt=0.06, tone_shape="sine", amp=0.20)
    # chamber map loop: contemplative drift
    pad_loop("music_map", 40.0, 98.0, [0, 2, 5, 7, 9, 12], 20,
             noise_amt=0.08, tone_shape="tri", amp=0.18)
    # focus loop (Signal, Causal): alert, pulsing
    pad_loop("music_focus", 36.0, 123.0, [0, 3, 5, 7, 10, 14], 24,
             noise_amt=0.05, tone_shape="sine", bass=True, amp=0.17)
    # structure loop (Forge, Perspective): measured, metallic shimmer
    pad_loop("music_structure", 36.0, 87.5, [0, 2, 3, 7, 8, 12], 18,
             noise_amt=0.10, tone_shape="tri", sparkle=True, amp=0.17)
    # tension loop (Paradox): quiet, restrained unease
    pad_loop("music_tension", 36.0, 92.5, [0, 1, 5, 6, 10, 13], 16,
             noise_amt=0.12, tone_shape="sine", sparkle=False, amp=0.16)
    # summit track: layered, evolving
    pad_loop("music_summit", 40.0, 104.0, [0, 3, 7, 10, 12, 17], 20,
             noise_amt=0.07, tone_shape="sine", bass=True, amp=0.20)
    # completion cue: warm resolution, 12s
    buf = np.zeros(int(12 * SR))
    chord = [220, 261.63, 329.63, 440]
    for i, fq in enumerate(chord):
        note(buf, fq, 0.3 + i * 0.35, 4.5, "sine", amp=0.22)
        note(buf, fq * 2, 0.35 + i * 0.35, 3.0, "sine", amp=0.07)
    note(buf, 523.25, 2.0, 3.0, "sine", amp=0.10)
    t = np.arange(len(buf)) / SR
    buf *= env_ad(t, a=0.2, r=2.5)
    write_ogg("music_complete", buf)

    # --- Ambience (loop-safe, 28s each) ------------------------------------
    pad_loop("amb_signal", 28.0, 65.4, [0, 7, 12, 19], 8, noise_amt=0.16,
             tone_shape="sine", bass=False, sparkle=True, amp=0.10)
    pad_loop("amb_forge", 28.0, 55.0, [0, 3, 7], 6, noise_amt=0.22,
             tone_shape="tri", bass=True, sparkle=False, amp=0.10)
    pad_loop("amb_perspective", 28.0, 73.4, [0, 5, 12, 17], 8, noise_amt=0.10,
             tone_shape="sine", bass=False, sparkle=True, amp=0.09)
    pad_loop("amb_causal", 28.0, 61.7, [0, 4, 9, 14], 10, noise_amt=0.14,
             tone_shape="sine", bass=True, sparkle=False, amp=0.10)
    pad_loop("amb_vault", 28.0, 49.0, [0, 1, 8], 6, noise_amt=0.18,
             tone_shape="sine", bass=False, sparkle=False, amp=0.09)
    pad_loop("amb_summit", 28.0, 82.4, [0, 7, 12, 16], 10, noise_amt=0.12,
             tone_shape="sine", bass=True, sparkle=True, amp=0.11)

    # --- SFX ----------------------------------------------------------------
    sfx("sfx_select", 0.22, lambda b: (note(b, 660, 0.0, 0.09, "sine", 0.5),
                                       note(b, 990, 0.06, 0.10, "sine", 0.3)))
    sfx("sfx_place", 0.3, lambda b: (note(b, 440, 0.0, 0.1, "sine", 0.45),
                                     note(b, 660, 0.09, 0.16, "sine", 0.45)))
    sfx("sfx_invalid", 0.3, lambda b: (note(b, 164, 0.0, 0.16, "square", 0.4),
                                      note(b, 147, 0.12, 0.16, "square", 0.32)))
    sfx("sfx_rotate", 0.28, lambda b: sweep(b, 300, 520, 0.0, 0.22, "sine", 0.4))
    sfx("sfx_connect", 0.35, lambda b: (note(b, 440, 0.0, 0.12, "sine", 0.4),
                                        note(b, 660, 0.1, 0.2, "sine", 0.42)))
    sfx("sfx_activate", 0.5, lambda b: sweep(b, 200, 900, 0.0, 0.42, "sine", 0.55))
    sfx("sfx_reset", 0.42, lambda b: (note(b, 520, 0.0, 0.1, "sine", 0.35),
                                      note(b, 390, 0.11, 0.1, "sine", 0.35),
                                      note(b, 260, 0.22, 0.16, "sine", 0.35)))
    sfx("sfx_hint", 0.6, lambda b: (note(b, 880, 0.0, 0.35, "sine", 0.3),
                                    note(b, 1320, 0.08, 0.4, "sine", 0.16)))
    sfx("sfx_discover", 0.7, lambda b: (note(b, 523, 0.0, 0.18, "sine", 0.35),
                                        note(b, 659, 0.13, 0.18, "sine", 0.35),
                                        note(b, 784, 0.26, 0.3, "sine", 0.35)))
    sfx("sfx_complete", 1.2, lambda b: (note(b, 392, 0.0, 0.7, "sine", 0.35),
                                        note(b, 494, 0.12, 0.7, "sine", 0.3),
                                        note(b, 587, 0.24, 0.8, "sine", 0.3),
                                        note(b, 784, 0.36, 0.8, "sine", 0.28)))
    sfx("sfx_unlock", 0.8, lambda b: (note(b, 1046, 0.0, 0.08, "tri", 0.4),
                                      sweep(b, 300, 1200, 0.1, 0.55, "sine", 0.35)))
    sfx("sfx_rule_change", 1.0, lambda b: (note(b, 415, 0.0, 0.5, "sine", 0.35),
                                           note(b, 440, 0.0, 0.5, "sine", 0.35),
                                           note(b, 622, 0.35, 0.5, "sine", 0.25)))
    sfx("sfx_achievement", 0.9, lambda b: (note(b, 659, 0.0, 0.2, "sine", 0.4),
                                           note(b, 880, 0.15, 0.2, "sine", 0.4),
                                           note(b, 1318, 0.3, 0.5, "sine", 0.35)))
    sfx("sfx_final", 2.6, lambda b: (sweep(b, 160, 640, 0.0, 1.4, "sine", 0.4),
                                     note(b, 523, 0.9, 1.4, "sine", 0.3),
                                     note(b, 659, 1.05, 1.4, "sine", 0.28),
                                     note(b, 784, 1.2, 1.4, "sine", 0.26)))

    print("AUDIO COMPLETE")


if __name__ == "__main__":
    main()
