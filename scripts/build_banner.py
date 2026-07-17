#!/usr/bin/env python3
"""
Banderole 3,00 m × 0,70 m — design élégant.
Titre sur une ligne, citation+Marka ensemble, programme en frise.
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

NAVY = "#0A2749"
NAVY_DARK = "#061A33"
NAVY_SOFT = "#143A66"
GOLD = "#D4891A"
ORANGE = "#E89520"
WHITE = "#FFFFFF"
MUTED = "#5C6B7A"
GRAY = "#2F3B4A"
LINE = "#E2E8F0"
GREEN = "#2D9B4A"
BLUE = "#1A6FB5"
CREAM = "#FFF9F0"

W, H = 3000, 700


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
      <path d="M-32 16 C-20 9 -8 9 0 13 C8 9 20 9 32 16 L32 24 C20 17 8 17 0 21 C-8 17 -20 17 -32 24 Z" fill="{NAVY}"/>
      <path d="M-27 16 C-16 11 -7 11 0 14 C7 11 16 11 27 16" fill="none" stroke="{GOLD}" stroke-width="2"/>
      <path d="M-22 -8 L-22 11 L22 11 L22 -8 L0 -28 Z" fill="{NAVY}"/>
      <path d="M-28 -6 L0 -32 L28 -6" fill="none" stroke="{GOLD}" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>
      <rect x="-5.5" y="-1" width="11" height="12" rx="1" fill="{GOLD}"/>
      <circle cx="-10" cy="-11" r="3.5" fill="{GOLD}"/>
      <circle cx="0" cy="-13" r="4.2" fill="{ORANGE}"/>
      <circle cx="10" cy="-11" r="3.5" fill="{GOLD}"/>
      <path d="M-15 -4.5 C-15 -8 -13 -11 -10 -11 C-7 -11 -5 -8 -5 -4.5 Z" fill="{GOLD}"/>
      <path d="M-5.5 -3 C-5.5 -9 -3 -13.5 0 -13.5 C3 -13.5 5.5 -9 5.5 -3 Z" fill="{ORANGE}"/>
      <path d="M5 -4.5 C5 -8 7 -11 10 -11 C13 -11 15 -8 15 -4.5 Z" fill="{GOLD}"/>
    </g>"""


def people(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="22" fill="{NAVY}"/>
      <circle cx="-8.5" cy="-4" r="4.8" fill="{GOLD}"/>
      <circle cy="-6.5" r="5.5" fill="{ORANGE}"/>
      <circle cx="8.5" cy="-4" r="4.8" fill="{GOLD}"/>
      <path d="M-15 12 C-15 5.5 -12 1 -8.5 1 C-5 1 -3 4.5 -2.5 8.5" fill="{GOLD}"/>
      <path d="M-7 14 C-7 4.5 -3.5 -1 0 -1 C3.5 -1 7 4.5 7 14 Z" fill="{ORANGE}"/>
      <path d="M2.5 8.5 C3 4.5 5 1 8.5 1 C12 1 15 5.5 15 12" fill="{GOLD}"/>
    </g>"""


def flame(cx, cy, r=11):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GOLD}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.05} {-r*0.42} {-r*0.35} {-r*0.15} {-r*0.7}
               C{-r*0.05} {-r*0.25} {r*0.2} {-r*0.4} {r*0.25} {-r*0.75}
               C{r*0.6} {-r*0.25} {r*0.55} {r*0.2} 0 {r*0.55} Z" fill="{WHITE}"/>
    </g>"""


def star(cx, cy, r=11):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{BLUE}"/>
      <path d="M0 {-r*0.55} L{r*0.14} {-r*0.15} L{r*0.55} {-r*0.15} L{r*0.22} {r*0.1}
               L{r*0.34} {r*0.5} L0 {r*0.25} L{-r*0.34} {r*0.5} L{-r*0.22} {r*0.1}
               L{-r*0.55} {-r*0.15} L{-r*0.14} {-r*0.15} Z" fill="{WHITE}"/>
    </g>"""


def leaf(cx, cy, r=11):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GREEN}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.05} {-r*0.5} {-r*0.4} 0 {-r*0.65}
               C{r*0.5} {-r*0.4} {r*0.5} {r*0.05} 0 {r*0.55} Z" fill="{WHITE}"/>
      <path d="M0 {r*0.45} V{-r*0.55}" stroke="{GREEN}" stroke-width="1.2"/>
    </g>"""


def book(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M-8 5.5 C-3.5 2.2 0 2.2 0 2.2 C0 2.2 3.5 2.2 8 5.5 V-5.5 C3.5 -8.5 0 -8.5 0 -8.5 C0 -8.5 -3.5 -8.5 -8 -5.5 Z" fill="{GOLD}"/>
      <path d="M0 -8.5 V2.2" stroke="{WHITE}" stroke-width="1"/>
    </g>"""


def pastor(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="15" fill="{WHITE}" opacity="0.14"/>
      <circle cy="-4" r="5" fill="{WHITE}"/>
      <path d="M-10 12 C-10 4 -6 0.5 0 0.5 C6 0.5 10 4 10 12 Z" fill="{WHITE}"/>
    </g>"""


def phone(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <rect x="-4.5" y="-8" width="9" height="16" rx="2" fill="none" stroke="{GOLD}" stroke-width="1.6"/>
      <circle cy="5.5" r="1" fill="{GOLD}"/>
    </g>"""


def timeline_schedule() -> str:
    """Elegant horizontal timeline — no ugly date cards."""
    days = [
        ("6", "ALAKAMISY", "15:00", "tolakandro"),
        ("7", "ZOMA", "15:00", "tolakandro"),
        ("8", "SABOTSY", "15:00", "tolakandro"),
        ("9", "ALAHADY", "09:00", "maraina"),
    ]
    # Timeline across center of banner
    y_line = 420
    xs = [520, 1170, 1820, 2470]
    parts = []

    # Background soft panel
    parts.append(
        f'<rect x="120" y="330" width="2760" height="200" rx="20" fill="{CREAM}" stroke="{LINE}" stroke-width="1.5"/>'
    )
    parts.append(
        T(W / 2, 358, "FANDAHARAM-POTOANA  ·  AOGOSITRA 2026",
          size=14, fill=MUTED, weight="700", anchor="middle", tracking="3")
    )

    # Connecting gold line
    parts.append(
        f'<line x1="{xs[0]}" y1="{y_line}" x2="{xs[-1]}" y2="{y_line}" '
        f'stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>'
    )

    for (num, name, time, period), x in zip(days, xs):
        parts.append(f"""
        <g>
          <circle cx="{x}" cy="{y_line}" r="32" fill="{GOLD}"/>
          {T(x, y_line + 10, num, size=28, fill=WHITE, weight="800", anchor="middle")}
          {T(x, y_line - 52, name, size=17, fill=NAVY, weight="800", anchor="middle", tracking="1.8")}
          {T(x, y_line + 62, time, size=22, fill=NAVY, weight="800", anchor="middle")}
          {T(x, y_line + 88, period, size=14, fill=MUTED, weight="600", anchor="middle", family="Open Sans")}
        </g>""")

    parts.append(
        T(W / 2, 515, "Fiangonana Jesosy Mpamonjy — Morafeno, Ambositra",
          size=14, fill=MUTED, weight="600", anchor="middle", family="Open Sans")
    )
    return "\n".join(parts)


def build_svg() -> str:
    crowd_path = ASSETS / "crowd-sunset-wide.jpg"
    if not crowd_path.exists():
        crowd_path = ASSETS / "crowd-sunset.png"
    crowd = data_uri(crowd_path)

    px, py, pw, ph = 2320, 48, 620, 95

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
  <title>Fitoriana Filazantsara Lehibe — 3m × 70cm</title>
  <desc>Design élégant — titre une ligne, citation+Marka, frise programme</desc>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F6FA"/>
    </linearGradient>
    <clipPath id="photoClip">
      <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"/>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <!-- TOP BAR -->
  <rect width="{W}" height="34" fill="{NAVY_DARK}"/>
  {T(W/2, 23, "FIANGONANA JESOSY MPAMONJY MORAFENO AMBOSITRA",
     size=16, fill=WHITE, weight="700", anchor="middle", tracking="5")}

  <!-- HEADER -->
  {logo(85, 100, 1.3)}

  <!-- TITLE ONE LINE via tspan -->
  <text x="160" y="92" font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="52" font-weight="800" letter-spacing="1.2">
    <tspan fill="{NAVY}">FITORIANA FILAZANTSARA </tspan>
    <tspan fill="{GOLD}">LEHIBE</tspan>
  </text>

  <!-- QUOTE + MARKA 16:15 together -->
  <text x="160" y="132" font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="17" font-weight="400" font-style="italic">
    <tspan fill="{GRAY}">“ Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, ka mitoria ny filazantsara amin'ny olombelona rehetra. ”</tspan>
    <tspan dx="12" fill="{GOLD}" font-style="normal" font-weight="700" font-family="Montserrat, DejaVu Sans, sans-serif">Marka 16:15</tspan>
  </text>

  <!-- Photo -->
  <g clip-path="url(#photoClip)">
    <image x="{px}" y="{py}" width="{pw}" height="{ph}"
           preserveAspectRatio="xMidYMid slice" xlink:href="{crowd}"/>
  </g>
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"
        fill="none" stroke="{GOLD}" stroke-width="2.5"/>

  <line x1="80" y1="155" x2="2920" y2="155" stroke="{LINE}" stroke-width="1.5"/>

  <!-- MID: invite | dates | benefits -->
  {people(100, 230, 1.0)}
  {T(145, 212, "Ny Mpitandrina sy ny fiangonana", size=15, fill=MUTED, weight="600", family="Open Sans")}
  {T(145, 240, "JESOSY MPAMONJY MORAFENO AMBOSITRA", size=19, fill=NAVY, weight="800")}
  {T(145, 266, "dia faly manasa antsika rehetra", size=15, fill=MUTED, weight="600", family="Open Sans")}

  <!-- Date hero -->
  {T(1180, 200, "Hanatrika ny Fitoriana Filazantsara Lehibe, izay atao ny",
     size=14, fill=MUTED, weight="600", anchor="middle", family="Open Sans")}
  <rect x="880" y="215" width="360" height="62" rx="14" fill="{GOLD}"/>
  {T(1060, 257, "6  ·  7  ·  8  ·  9", size=34, fill=NAVY, weight="800", anchor="middle")}
  {T(1285, 257, "AOGOSITRA 2026", size=30, fill=NAVY, weight="800")}

  <!-- Benefits -->
  {flame(1750, 210)}
  {T(1775, 215, "Ho famonjena fanahin'olona", size=17, fill=NAVY, weight="700")}
  {star(1750, 250)}
  {T(1775, 255, "Ho fanasitranana ny aretina", size=17, fill=NAVY, weight="700")}
  {leaf(1750, 290)}
  {T(1775, 295, "Ho fiainana mandrakizay ho anao", size=17, fill=NAVY, weight="700")}

  <!-- TIMELINE SCHEDULE -->
  {timeline_schedule()}

  <!-- COMPACT FOOTER -->
  <rect x="0" y="555" width="{W}" height="145" fill="{NAVY_DARK}"/>
  <rect x="0" y="555" width="{W}" height="5" fill="{GOLD}"/>

  {T(90, 610, "Anasana antsika rehetra — tongava handray ny anjaranao!",
     size=24, fill=GOLD, family="Dancing Script", weight="700")}
  {T(90, 645, "Fotoana lehibe ho an'ny fanahy, ny fanasitranana ary ny fiainana mandrakizay.",
     size=14, fill="#C8D4E4", weight="500", family="Open Sans")}

  <rect x="1680" y="580" width="1240" height="100" rx="12" fill="{NAVY_SOFT}"/>
  <rect x="1680" y="580" width="6" height="100" fill="{GOLD}"/>
  {pastor(1735, 630, 1.2)}
  {T(1780, 610, "Ny Mpitandrina", size=13, fill=GOLD, weight="600")}
  {T(1780, 638, "RANDRIANARIZANANY Lovasoa Fenomanana", size=18, fill=WHITE, weight="700")}
  {phone(1790, 665)}
  {T(1815, 670, "038 92 546 27   ·   033 20 968 28", size=16, fill=WHITE, weight="600")}
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

    svg = OUT / "banderole-3m-x-70cm.svg"
    svg.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {svg}")

    outlined = OUT / "banderole-3m-x-70cm-outlined.svg"
    outline(svg, outlined)
    pdf = OUT / "banderole-3m-x-70cm.pdf"
    inkscape(outlined, pdf, typ="pdf")
    preview = PREVIEWS / "banderole-preview.png"
    inkscape(svg, preview, typ="png", width=3600)
    hd = OUT / "banderole-3m-x-70cm-150dpi.png"
    inkscape(svg, hd, typ="png", dpi=150)
    for p in [svg, outlined, pdf, preview]:
        shutil.copy(p, ARTIFACTS / p.name)
    from PIL import Image
    print("preview", Image.open(preview).size)


if __name__ == "__main__":
    main()
