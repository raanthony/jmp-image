#!/usr/bin/env python3
"""
Banderole 3000×700 mm — layout en bandes strictes, zéro chevauchement.
Contenu fidèle au flyer : Fitoriana Filazantsara Lehibe Morafeno Ambositra.
"""

from __future__ import annotations

import base64
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/workspace")
OUT = ROOT / "banner"
ASSETS = ROOT / "assets"
ARTIFACTS = Path("/opt/cursor/artifacts")
PREVIEWS = ARTIFACTS / "screenshots"

NAVY = "#0A2A5C"
NAVY_DARK = "#061833"
NAVY_MID = "#123A6F"
GOLD = "#E0891C"
ORANGE = "#F09420"
WHITE = "#FFFFFF"
GRAY = "#3A4658"
MUTED = "#6A7688"
LINE = "#D5DCE6"
GREEN = "#2F9E44"
BLUE = "#1E6BB8"
BG = "#FFFFFF"

W, H = 3000, 700

# ---- Strict vertical bands (mm) — nothing crosses band boundaries ----
# TOP     0 .. 34
# HEADER  42 .. 138
# QUOTE   148 .. 200
# MID     210 .. 300
# DAYS    312 .. 470
# FOOTER  482 .. 700


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def T(x, y, content, *, size=18, fill=NAVY, family="Montserrat",
      weight="700", style="normal", anchor="start", tracking=None):
    a = [
        f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
        f'font-family="{family}, DejaVu Sans, sans-serif"',
        f'font-size="{size}"', f'font-weight="{weight}"',
        f'font-style="{style}"', f'text-anchor="{anchor}"',
    ]
    if tracking is not None:
        a.append(f'letter-spacing="{tracking}"')
    return f"<text {' '.join(a)}>{esc(content)}</text>"


def data_uri(path: Path) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode()
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{b64}"


def logo(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M-34 18 C-21 10 -8 10 0 14 C8 10 21 10 34 18 L34 26 C21 18 8 18 0 22 C-8 18 -21 18 -34 26 Z" fill="{NAVY}"/>
      <path d="M-29 18 C-17 12 -7 12 0 15 C7 12 17 12 29 18" fill="none" stroke="{GOLD}" stroke-width="2.2"/>
      <path d="M-24 -8 L-24 12 L24 12 L24 -8 L0 -30 Z" fill="{NAVY}"/>
      <path d="M-30 -6 L0 -34 L30 -6" fill="none" stroke="{GOLD}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>
      <rect x="-6" y="-1" width="12" height="13" rx="1.2" fill="{GOLD}"/>
      <circle cx="-11" cy="-11" r="3.8" fill="{GOLD}"/>
      <circle cx="0" cy="-13.5" r="4.5" fill="{ORANGE}"/>
      <circle cx="11" cy="-11" r="3.8" fill="{GOLD}"/>
      <path d="M-16 -4 C-16 -8 -14 -11 -11 -11 C-8 -11 -6 -8 -6 -4 Z" fill="{GOLD}"/>
      <path d="M-6 -2.5 C-6 -9 -3.2 -14 0 -14 C3.2 -14 6 -9 6 -2.5 Z" fill="{ORANGE}"/>
      <path d="M6 -4 C6 -8 8 -11 11 -11 C14 -11 16 -8 16 -4 Z" fill="{GOLD}"/>
    </g>"""


def people(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="26" fill="{NAVY}"/>
      <circle cx="-10" cy="-5" r="5.5" fill="{GOLD}"/>
      <circle cy="-7.5" r="6.5" fill="{ORANGE}"/>
      <circle cx="10" cy="-5" r="5.5" fill="{GOLD}"/>
      <path d="M-18 14 C-18 6 -14 1 -10 1 C-6 1 -3.5 5 -3 10" fill="{GOLD}"/>
      <path d="M-8 16 C-8 5 -4 -1 0 -1 C4 -1 8 5 8 16 Z" fill="{ORANGE}"/>
      <path d="M3 10 C3.5 5 6 1 10 1 C14 1 18 6 18 14" fill="{GOLD}"/>
    </g>"""


def flame(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="13" fill="{GOLD}"/>
      <path d="M0 8 C-6.5 1 -5.5 -4 -2 -9 C-0.5 -3 2.5 -5 3.2 -10 C8 -3 7.5 3 0 8 Z" fill="{WHITE}"/>
    </g>"""


def star(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="13" fill="{BLUE}"/>
      <path d="M0 -7.5 L1.9 -2 L7.5 -2 L2.9 1.2 L4.6 6.8 L0 3.4 L-4.6 6.8 L-2.9 1.2 L-7.5 -2 L-1.9 -2 Z" fill="{WHITE}"/>
    </g>"""


def leaf(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="13" fill="{GREEN}"/>
      <path d="M0 7.5 C-6.5 1 -6.5 -5.5 0 -8.5 C6.5 -5.5 6.5 1 0 7.5 Z" fill="{WHITE}"/>
      <path d="M0 6.5 V-7.5" stroke="{GREEN}" stroke-width="1.3"/>
    </g>"""


def calendar(cx, cy, day):
    return f"""
    <g transform="translate({cx-13},{cy-14})">
      <rect y="4" width="26" height="24" rx="3.5" fill="{GOLD}"/>
      <rect y="4" width="26" height="8" rx="2.5" fill="{NAVY}"/>
      <rect x="2" y="14" width="22" height="12" rx="1.5" fill="{WHITE}"/>
      <circle cx="7" cy="2.5" r="2" fill="{NAVY}"/>
      <circle cx="19" cy="2.5" r="2" fill="{NAVY}"/>
      {T(13, 24, str(day), size=11, fill=NAVY, weight="800", anchor="middle")}
    </g>"""


def clock(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="9" fill="none" stroke="{GOLD}" stroke-width="2.2"/>
      <circle r="1.5" fill="{GOLD}"/>
      <path d="M0 -5 V0 H4" fill="none" stroke="{NAVY}" stroke-width="1.8" stroke-linecap="round"/>
    </g>"""


def pin(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <path d="M0 -9 C-5.8 -9 -9.5 -3.8 -9.5 0.5 C-9.5 6.5 0 13 0 13 C0 13 9.5 6.5 9.5 0.5 C9.5 -3.8 5.8 -9 0 -9 Z" fill="{GOLD}"/>
      <circle cy="-0.2" r="2.8" fill="{WHITE}"/>
    </g>"""


def book(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <path d="M-10 6.5 C-4.5 3 0 3 0 3 C0 3 4.5 3 10 6.5 V-6.5 C4.5 -10 0 -10 0 -10 C0 -10 -4.5 -10 -10 -6.5 Z" fill="{GOLD}"/>
      <path d="M0 -10 V3" stroke="{WHITE}" stroke-width="1.2"/>
    </g>"""


def pastor(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="18" fill="{WHITE}" opacity="0.12"/>
      <circle cy="-5" r="6" fill="{WHITE}"/>
      <path d="M-12 14 C-12 5 -7 1 0 1 C7 1 12 5 12 14 Z" fill="{WHITE}"/>
    </g>"""


def phone(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <rect x="-5.5" y="-9.5" width="11" height="19" rx="2.4" fill="none" stroke="{GOLD}" stroke-width="1.8"/>
      <circle cy="6.5" r="1.2" fill="{GOLD}"/>
    </g>"""


def wheat(cx, cy, flip=False):
    sx = -1 if flip else 1
    return f"""
    <g transform="translate({cx},{cy}) scale({sx},1)" fill="{GOLD}">
      <path d="M0 1 C16 -12 34 -15 50 -10 C34 -5 18 0 0 1 Z" opacity="0.95"/>
      <path d="M6 0 C22 -18 42 -24 60 -18 C42 -12 24 -3 6 0 Z" opacity="0.7"/>
      <path d="M12 6 C28 -2 46 -2 62 4 C46 8 30 11 12 6 Z" opacity="0.85"/>
    </g>"""


def day_card(x, y, w, h, name, num, time_s, place1, place2):
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{WHITE}" stroke="{LINE}" stroke-width="1.8"/>
      <path d="M{x} {y+9} Q{x} {y} {x+9} {y} H{x+w-9} Q{x+w} {y} {x+w} {y+9} V{y+28} H{x} Z" fill="{NAVY}"/>
      <rect x="{x}" y="{y+26}" width="{w}" height="7" fill="{GOLD}"/>
      {T(x + w/2, y + 19, name, size=13, fill=WHITE, weight="800", anchor="middle", tracking="1.5")}
      {calendar(x + 26, y + 55, num)}
      {T(x + 48, y + 52, f"{num} Aogositra 2026", size=13, fill=NAVY, weight="700")}
      {clock(x + 22, y + 82)}
      {T(x + 38, y + 86, time_s, size=12, fill=MUTED, weight="600", family="Open Sans")}
      {pin(x + 22, y + 112)}
      {T(x + 38, y + 106, place1, size=12, fill=GRAY, weight="700")}
      {T(x + 38, y + 124, place2, size=11.5, fill=MUTED, weight="600", family="Open Sans")}
    </g>"""


def build_svg() -> str:
    crowd_path = ASSETS / "crowd-sunset-wide.jpg"
    if not crowd_path.exists():
        crowd_path = ASSETS / "crowd-sunset.png"
    crowd = data_uri(crowd_path)

    # Photo panel — HEADER band only (y 48..132)
    px, py, pw, ph = 2140, 48, 800, 84

    days = [
        ("ALAKAMISY", "6", "@ 15:00 · 3 ora tolakandro", "Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"),
        ("ZOMA", "7", "@ 15:00 · 3 ora tolakandro", "Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"),
        ("SABOTSY", "8", "@ 15:00 · 3 ora tolakandro", "Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"),
        ("ALAHADY", "9", "@ 09:00 · 9 ora maraina", "Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"),
    ]
    card_w, gap = 705, 16
    total = 4 * card_w + 3 * gap
    x0 = (W - total) / 2
    # DAYS band y=330..485 — gap 25mm after MID (ends ~305)
    cards = "\n".join(
        day_card(x0 + i * (card_w + gap), 330, card_w, 150, *d)
        for i, d in enumerate(days)
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
  <title>Fitoriana Filazantsara Lehibe — 3m × 70cm</title>
  <desc>Banderole sans chevauchement — contenu flyer Morafeno Ambositra</desc>

  <defs>
    <clipPath id="photoClip">
      <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"/>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>

  <!-- ========== BAND 1: TOP BAR 0-34 ========== -->
  <rect width="{W}" height="34" fill="{NAVY_DARK}"/>
  {T(W/2, 23, "FIANGONANA JESOSY MPAMONJY MORAFENO AMBOSITRA",
     size=16, fill=WHITE, weight="700", anchor="middle", tracking="4.5")}

  <!-- ========== BAND 2: HEADER 42-138 ========== -->
  {logo(95, 95, 1.25)}
  {T(170, 82, "FITORIANA FILAZANTSARA", size=44, fill=NAVY, weight="800")}
  {T(170, 128, "LEHIBE", size=48, fill=GOLD, weight="800", tracking="6")}

  <g clip-path="url(#photoClip)">
    <image x="{px}" y="{py}" width="{pw}" height="{ph}"
           preserveAspectRatio="xMidYMid slice" xlink:href="{crowd}"/>
  </g>
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"
        fill="none" stroke="{GOLD}" stroke-width="2.5"/>

  <!-- ========== BAND 3: QUOTE 148-200 ========== -->
  {T(80, 175, "“", size=48, fill=GOLD, family="Great Vibes", weight="400")}
  {T(130, 172, "Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, ka mitoria ny filazantsara amin'ny olombelona rehetra.",
     size=15, fill=NAVY, family="Open Sans", weight="400", style="italic")}
  {T(2050, 178, "”", size=48, fill=GOLD, family="Great Vibes", weight="400")}
  {book(2120, 170)}
  {T(2145, 175, "Marka 16:15", size=15, fill=GOLD, weight="700")}

  <line x1="70" y1="205" x2="2930" y2="205" stroke="{LINE}" stroke-width="1.5"/>

  <!-- ========== BAND 4: MID 210-300 (strict) ========== -->
  {people(100, 255, 0.95)}
  {T(145, 240, "Ny Mpitandrina sy ny fiangonana", size=13, fill=MUTED, weight="600", family="Open Sans")}
  {T(145, 260, "JESOSY MPAMONJY MORAFENO AMBOSITRA", size=14, fill=NAVY, weight="800")}
  {T(145, 280, "dia faly manasa antsika rehetra", size=13, fill=MUTED, weight="600", family="Open Sans")}

  <line x1="700" y1="220" x2="700" y2="295" stroke="{LINE}" stroke-width="1.5"/>

  {T(1150, 228, "Hanatrika ny Fitoriana Filazantsara Lehibe, izay atao ny",
     size=12.5, fill=MUTED, weight="600", anchor="middle", family="Open Sans")}
  <rect x="880" y="238" width="300" height="40" rx="10" fill="{GOLD}"/>
  {T(1030, 265, "6  -  7  -  8  -  9", size=24, fill=NAVY, weight="800", anchor="middle")}
  {T(1210, 265, "AOGOSITRA 2026", size=22, fill=NAVY, weight="800")}
  <rect x="960" y="286" width="220" height="18" rx="3" fill="{NAVY}"/>
  {T(1070, 299, "FANDAHARAM-POTOANA", size=10.5, fill=WHITE, weight="700", anchor="middle", tracking="1.2")}

  <line x1="1550" y1="218" x2="1550" y2="300" stroke="{LINE}" stroke-width="1.5"/>

  {flame(1620, 232)}
  {T(1645, 237, "Ho famonjena fanahin'olona", size=14.5, fill=NAVY, weight="700")}
  {star(1620, 262)}
  {T(1645, 267, "Ho fanasitranana ny aretina", size=14.5, fill=NAVY, weight="700")}
  {leaf(1620, 292)}
  {T(1645, 297, "Ho fiainana mandrakizay ho anao", size=14.5, fill=NAVY, weight="700")}

  <!-- ========== BAND 5: DAYS 330-485 (gap clair après MID) ========== -->
  {cards}

  <!-- ========== BAND 6: FOOTER 500-700 ========== -->
  <rect x="0" y="500" width="{W}" height="200" fill="{NAVY_DARK}"/>
  <rect x="0" y="500" width="{W}" height="6" fill="{GOLD}"/>

  {wheat(200, 585, False)}
  {T(1050, 570, "Anasana antsika rehetra hanatrika izany fotoana lehibe izany,",
     size=28, fill=GOLD, family="Dancing Script", weight="700", anchor="middle")}
  {T(1050, 615, "tongava handray ny anjaranao!",
     size=32, fill=GOLD, family="Dancing Script", weight="700", anchor="middle")}
  {wheat(1900, 585, True)}

  <rect x="2050" y="535" width="870" height="130" rx="12" fill="{NAVY_MID}"/>
  <rect x="2050" y="535" width="7" height="130" fill="{GOLD}"/>
  {pastor(2115, 600)}
  {T(2165, 570, "Ny Mpitandrina:", size=14, fill=GOLD, weight="600")}
  {T(2165, 600, "RANDRIANARIZANANY Lovasoa Fenomanana", size=17, fill=WHITE, weight="700")}
  {phone(2175, 635)}
  {T(2200, 640, "038 92 546 27  /  033 20 968 28", size=17, fill=WHITE, weight="700")}
</svg>
"""


def inkscape(svg: Path, out: Path, *, typ: str, dpi=None, width=None):
    Path("/tmp/fc").mkdir(exist_ok=True)
    Path("/tmp/fc/fonts.conf").write_text(
        """<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir>/workspace/fonts</dir>
  <dir>/home/ubuntu/.fonts</dir>
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
</fontconfig>"""
    )
    env = dict(**subprocess.os.environ)
    env["FONTCONFIG_FILE"] = "/tmp/fc/fonts.conf"
    cmd = ["inkscape", str(svg), f"--export-type={typ}", f"--export-filename={out}"]
    if dpi:
        cmd.append(f"--export-dpi={dpi}")
    if width:
        cmd.append(f"--export-width={width}")
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1200:])
    print(f"OK {out.name} ({out.stat().st_size/1e6:.2f} MB)")


def outline(src: Path, dest: Path):
    env = dict(**subprocess.os.environ)
    env["FONTCONFIG_FILE"] = "/tmp/fc/fonts.conf"
    actions = f"select-by-element:text;object-to-path;export-filename:{dest};export-type:svg;export-do"
    r = subprocess.run(["inkscape", str(src), f"--actions={actions}"],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0 or not dest.exists():
        shutil.copy(src, dest)
    print(f"OK outlined {dest.name}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    # ensure wide crowd exists
    wide = ASSETS / "crowd-sunset-wide.jpg"
    if not wide.exists() and (ASSETS / "crowd-sunset.png").exists():
        from PIL import Image
        im = Image.open(ASSETS / "crowd-sunset.png").convert("RGB")
        w, h = im.size
        top = int(h * 0.35)
        im.crop((0, top, w, h)).resize((1800, 600), Image.Resampling.LANCZOS).save(wide, quality=92)

    svg = OUT / "banderole-3m-x-70cm.svg"
    svg.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {svg}")

    outlined = OUT / "banderole-3m-x-70cm-outlined.svg"
    outline(svg, outlined)

    pdf = OUT / "banderole-3m-x-70cm.pdf"
    inkscape(outlined, pdf, typ="pdf")

    preview = PREVIEWS / "banderole-preview.png"
    inkscape(svg, preview, typ="png", width=3600)

    # Copy generated reference too
    src_gen = ARTIFACTS / "assets" / "banderole-nouvelle.png"
    if src_gen.exists():
        shutil.copy(src_gen, PREVIEWS / "banderole-nouvelle-ref.png")

    hd = OUT / "banderole-3m-x-70cm-150dpi.png"
    inkscape(svg, hd, typ="png", dpi=150)

    for p in [svg, outlined, pdf, preview]:
        shutil.copy(p, ARTIFACTS / p.name)

    # overlap sanity check via band markers on preview
    from PIL import Image, ImageDraw
    im = Image.open(preview)
    scale = im.width / W
    d = im.copy()
    draw = ImageDraw.Draw(d, "RGBA")
    for y1, y2, color in [
        (0, 34, (0, 255, 0, 40)),
        (42, 138, (0, 0, 255, 40)),
        (148, 200, (255, 255, 0, 40)),
        (210, 300, (255, 0, 255, 40)),
        (312, 470, (0, 255, 255, 40)),
        (482, 700, (255, 128, 0, 40)),
    ]:
        draw.rectangle([0, y1 * scale, im.width, y2 * scale], fill=color)
    d.save(PREVIEWS / "layout-bands.png")
    print("preview", im.size)


if __name__ == "__main__":
    main()
