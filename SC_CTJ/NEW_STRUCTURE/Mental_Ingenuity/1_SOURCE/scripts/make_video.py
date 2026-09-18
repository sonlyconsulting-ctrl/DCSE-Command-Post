#!/usr/bin/env python3
"""Opening cinematic video for Mental Ingenuity.

Fully original programmatic animation: abstract obsidian chamber awakening
with gold and emerald energy. No text is rendered into frames (brand text is
overlaid in HTML to guarantee correct spelling). 1920x1080, 24fps, 16s,
H.264 MP4 + VP9 WebM.
"""
import math
import os
import random
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1920, 1080
FPS = 24
DUR = 16.0
N = int(FPS * DUR)
OUT = os.path.join(os.path.dirname(__file__), "..", "public", "media", "video")
os.makedirs(OUT, exist_ok=True)

GOLD = (201, 168, 76)
EMERALD = (47, 212, 138)
SILVER = (159, 178, 200)
NAVY_TOP = (10, 15, 30)
NAVY_BOT = (4, 6, 12)


def ease(x):
    return x * x * (3 - 2 * x)


def clamp01(x):
    return max(0.0, min(1.0, x))


def phase(t, a, b):
    return clamp01((t - a) / (b - a))


# --- precomputed sprites ----------------------------------------------------
def radial_sprite(size, rgb, peak=255):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    arr = np.zeros((size, size, 4), dtype=np.uint8)
    yy, xx = np.mgrid[0:size, 0:size]
    c = size / 2
    d = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / c
    a = np.clip(1 - d, 0, 1) ** 2.2
    arr[..., 0] = rgb[0]
    arr[..., 1] = rgb[1]
    arr[..., 2] = rgb[2]
    arr[..., 3] = (a * peak).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


GLOW_GOLD = radial_sprite(300, GOLD)
GLOW_EMERALD = radial_sprite(300, EMERALD)
GLOW_SOFT = radial_sprite(700, (30, 60, 70), 90)

# background gradient
bg = np.zeros((H, W, 3), dtype=np.uint8)
for y in range(H):
    f = y / H
    bg[y, :] = [int(NAVY_TOP[i] * (1 - f) + NAVY_BOT[i] * f) for i in range(3)]
BG = Image.fromarray(bg, "RGB")

# vignette mask
yy, xx = np.mgrid[0:H, 0:W]
dc = np.sqrt(((xx - W / 2) / (W * 0.72)) ** 2 + ((yy - H * 0.52) / (H * 0.78)) ** 2)
VIGN = np.clip(1.15 - dc, 0.25, 1.0).astype(np.float32)

rng = random.Random(42)
PARTICLES = [(rng.uniform(0, W), rng.uniform(H * 0.2, H), rng.uniform(6, 26),
              rng.uniform(4, 16), rng.uniform(0, 1)) for _ in range(90)]

CX, CY = W // 2, int(H * 0.52)


def paste_glow(layer, sprite, x, y, scale, alpha):
    if alpha <= 0.01:
        return
    s = int(sprite.width * scale)
    if s < 4:
        return
    sp = sprite.resize((s, s), Image.BILINEAR)
    if alpha < 1:
        a = sp.getchannel("A").point(lambda v: int(v * alpha))
        sp.putalpha(a)
    layer.alpha_composite(sp, (int(x - s / 2), int(y - s / 2)))


def draw_frame(t):
    img = BG.copy()
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)

    awaken = phase(t, 0.5, 3.5)
    lines_p = phase(t, 2.5, 7.0)
    rings_p = phase(t, 6.0, 11.0)
    gate_p = phase(t, 10.0, 14.0)

    # central soft depth glow
    paste_glow(layer, GLOW_SOFT, CX, CY, 2.6, 0.5 + 0.4 * awaken)

    # architectural radial pathways (gold), drawn outward over time
    n_rays = 14
    for i in range(n_rays):
        ang = math.pi * (i / (n_rays - 1)) + math.pi  # upper semicircle fan
        seg = ease(clamp01(lines_p * 1.4 - (i % 4) * 0.08))
        if seg <= 0.01:
            continue
        r0 = 130
        r1 = r0 + seg * 1150
        x0 = CX + math.cos(ang) * r0
        y0 = CY + math.sin(ang) * r0 * 0.62
        x1 = CX + math.cos(ang) * r1
        y1 = CY + math.sin(ang) * r1 * 0.62
        dr.line([(x0, y0), (x1, y1)], fill=GOLD + (70,), width=2)
        # traveling emerald pulse along the ray
        if lines_p > 0.25:
            pp = (t * 0.35 + i * 0.13) % 1.0
            px = x0 + (x1 - x0) * pp
            py = y0 + (y1 - y0) * pp
            paste_glow(layer, GLOW_EMERALD, px, py, 0.22, 0.5 * seg)

    # horizon floor lines (perspective grid), faint
    if lines_p > 0.1:
        for j, fy in enumerate([0.66, 0.72, 0.8, 0.9]):
            a = int(46 * ease(phase(lines_p, j * 0.08, j * 0.08 + 0.5)))
            if a > 2:
                dr.line([(0, int(H * fy)), (W, int(H * fy))], fill=SILVER + (a,), width=1)

    # rotating concentric mechanism rings
    for k, (rad, spd, wdt) in enumerate([(240, 0.35, 3), (340, -0.22, 2), (470, 0.14, 2), (620, -0.09, 1)]):
        rp = ease(phase(rings_p, k * 0.12, k * 0.12 + 0.6))
        if rp <= 0.01:
            continue
        start = t * spd * 90 + k * 47
        sweep = 70 + 220 * rp
        box = [CX - rad, CY - rad * 0.62, CX + rad, CY + rad * 0.62]
        col = GOLD if k % 2 == 0 else SILVER
        dr.arc(box, start, start + sweep, fill=col + (int(120 * rp),), width=wdt)
        dr.arc(box, start + 180, start + 180 + sweep * 0.7, fill=col + (int(70 * rp),), width=wdt)

    # monolith silhouettes rising on both flanks
    mono_p = ease(phase(t, 8.5, 13.0))
    if mono_p > 0:
        for side in (-1, 1):
            for m in range(4):
                mw = 120 - m * 18
                mh = (360 + m * 90) * mono_p
                mx = CX + side * (330 + m * 205) - mw / 2
                my = H * 0.86 - mh
                dr.rectangle([mx, my, mx + mw, H * 0.86], fill=(7, 10, 18, 235))
                dr.line([(mx, my), (mx + mw, my)], fill=GOLD + (int(150 * mono_p),), width=2)
                dr.line([(mx + side * 0, my), (mx + (mw if side > 0 else 0), H * 0.86)],
                        fill=SILVER + (int(60 * mono_p),), width=1)

    # the gate: stable final composition
    if gate_p > 0:
        gw, gh = 430, 560
        gx0, gy0 = CX - gw // 2, CY - gh // 2 + 40
        gx1, gy1 = CX + gw // 2, CY + gh // 2 + 40
        gp = ease(gate_p)
        dr.rectangle([gx0, gy0, gx1, gy1], outline=GOLD + (int(200 * gp),), width=4)
        inset = 26
        dr.rectangle([gx0 + inset, gy0 + inset, gx1 - inset, gy1 - inset],
                     outline=SILVER + (int(140 * gp),), width=2)
        paste_glow(layer, GLOW_EMERALD, CX, CY + 40, 1.9 * gp, 0.75 * gp)
        # threshold beams locking in
        for q in range(3):
            qp = ease(phase(gate_p, 0.3 + q * 0.15, 0.55 + q * 0.15))
            if qp > 0:
                yy2 = gy0 + inset + (gh - 2 * inset) * (q + 1) / 4
                dr.line([(gx0 + inset, yy2), (gx0 + inset + (gw - 2 * inset) * qp, yy2)],
                        fill=EMERALD + (int(160 * qp),), width=2)

    # drifting particles
    if awaken > 0:
        for px0, py0, sz, spd, off in PARTICLES:
            py = (py0 - t * spd * 6) % (H * 0.85) + H * 0.08
            a = 0.14 + 0.1 * math.sin(t * 1.3 + off * 7)
            paste_glow(layer, GLOW_GOLD, px0, py, sz / 90.0, a * awaken)

    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

    # fade in from darkness
    fi = ease(phase(t, 0.0, 1.2))
    if fi < 1:
        img = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), img, fi)

    # vignette
    arr = np.asarray(img, dtype=np.float32)
    arr *= VIGN[..., None]
    return np.clip(arr, 0, 255).astype(np.uint8)


def main():
    mp4 = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
         "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
         os.path.join(OUT, "opening.mp4")],
        stdin=subprocess.PIPE)
    webm = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-c:v", "libvpx-vp9", "-b:v", "1400k",
         "-deadline", "realtime", "-cpu-used", "4",
         os.path.join(OUT, "opening.webm")],
        stdin=subprocess.PIPE)
    last = None
    for i in range(N):
        t = i / FPS
        frame = draw_frame(t)
        last = frame
        mp4.stdin.write(frame.tobytes())
        webm.stdin.write(frame.tobytes())
        if i % 48 == 0:
            print(f"frame {i}/{N}", flush=True)
    mp4.stdin.close()
    webm.stdin.close()
    mp4.wait()
    webm.wait()
    Image.fromarray(last).save(os.path.join(OUT, "poster.jpg"), quality=88)
    print("VIDEO COMPLETE")


if __name__ == "__main__":
    main()
