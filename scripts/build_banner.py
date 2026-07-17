#!/usr/bin/env python3
"""
Banderole premium 3,00 × 0,70 m — flyer-inspired.
Photo mains pleine hauteur à droite + dégradé, timeline iconique.
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

NAVY = "#071A36"
NAVY_MID = "#0E2F58"
GOLD = "#C97B14"
GOLD2 = "#E59A2A"
ORANGE = "#E08A1A"
WHITE = "#FFFFFF"
IVORY = "#FFFCFA"
MUTED = "#667384"
INK = "#1A2430"
LINE = "#E8EEF5"
GREEN = "#278A3D"
BLUE = "#1B6CA8"

W, H = 3000, 700
PHOTO_X = 2080  # photo more to the right — background, not dominant
PHOTO_W = W - PHOTO_X


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
      <path d="M-34 18 C-21 10 -8 10 0 14.5 C8 10 21 10 34 18 L34 27 C21 19 8 19 0 23.5 C-8 19 -21 19 -34 27 Z" fill="{NAVY}"/>
      <path d="M-29 18 C-17 12.5 -7 12.5 0 15.5 C7 12.5 17 12.5 29 18" fill="none" stroke="{GOLD}" stroke-width="2.2"/>
      <path d="M-24 -9 L-24 12 L24 12 L24 -9 L0 -31 Z" fill="{NAVY}"/>
      <path d="M-30 -7 L0 -35 L30 -7" fill="none" stroke="{GOLD}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>
      <rect x="-6" y="-1" width="12" height="13" rx="1.2" fill="{GOLD}"/>
      <circle cx="-11" cy="-12" r="3.8" fill="{GOLD}"/>
      <circle cx="0" cy="-14.5" r="4.5" fill="{ORANGE}"/>
      <circle cx="11" cy="-12" r="3.8" fill="{GOLD}"/>
      <path d="M-16.5 -5 C-16.5 -8.8 -14.2 -12 -11 -12 C-7.8 -12 -5.5 -8.8 -5.5 -5 Z" fill="{GOLD}"/>
      <path d="M-6 -3.2 C-6 -9.5 -3.2 -14.5 0 -14.5 C3.2 -14.5 6 -9.5 6 -3.2 Z" fill="{ORANGE}"/>
      <path d="M5.5 -5 C5.5 -8.8 7.8 -12 11 -12 C14.2 -12 16.5 -8.8 16.5 -5 Z" fill="{GOLD}"/>
    </g>"""


def people(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="23" fill="{NAVY}"/>
      <circle cx="-9" cy="-4.5" r="5" fill="{GOLD}"/>
      <circle cy="-7" r="5.8" fill="{ORANGE}"/>
      <circle cx="9" cy="-4.5" r="5" fill="{GOLD}"/>
      <path d="M-16 13 C-16 6 -13 1 -9 1 C-5 1 -3 5 -2.5 9" fill="{GOLD}"/>
      <path d="M-7.5 14.5 C-7.5 5 -4 -1 0 -1 C4 -1 7.5 5 7.5 14.5 Z" fill="{ORANGE}"/>
      <path d="M2.5 9 C3 5 5.5 1 9 1 C13 1 16 6 16 13" fill="{GOLD}"/>
    </g>"""


def ico_flame(cx, cy, r=12.5):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GOLD}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.08} {-r*0.4} {-r*0.3} {-r*0.12} {-r*0.68}
               C{-r*0.02} {-r*0.22} {r*0.18} {-r*0.38} {r*0.22} {-r*0.72}
               C{r*0.58} {-r*0.22} {r*0.52} {r*0.22} 0 {r*0.55} Z" fill="{WHITE}"/>
    </g>"""


def ico_star(cx, cy, r=12.5):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{BLUE}"/>
      <path d="M0 {-r*0.55} L{r*0.15} {-r*0.14} L{r*0.55} {-r*0.14} L{r*0.22} {r*0.12}
               L{r*0.34} {r*0.52} L0 {r*0.26} L{-r*0.34} {r*0.52} L{-r*0.22} {r*0.12}
               L{-r*0.55} {-r*0.14} L{-r*0.15} {-r*0.14} Z" fill="{WHITE}"/>
    </g>"""


def ico_leaf(cx, cy, r=12.5):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GREEN}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.08} {-r*0.5} {-r*0.4} 0 {-r*0.65}
               C{r*0.5} {-r*0.4} {r*0.5} {r*0.08} 0 {r*0.55} Z" fill="{WHITE}"/>
      <path d="M0 {r*0.42} V{-r*0.55}" stroke="{GREEN}" stroke-width="1.3"/>
    </g>"""


def ico_cal(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <rect x="-10" y="-7" width="20" height="16" rx="2.5" fill="{GOLD}"/>
      <rect x="-10" y="-7" width="20" height="5.5" rx="2" fill="{NAVY}"/>
      <rect x="-7.5" y="0" width="15" height="7" rx="1" fill="{WHITE}"/>
      <circle cx="-4.5" cy="-9.5" r="1.5" fill="{NAVY}"/>
      <circle cx="4.5" cy="-9.5" r="1.5" fill="{NAVY}"/>
    </g>"""


def ico_clock(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="9.5" fill="{WHITE}" stroke="{GOLD}" stroke-width="2.2"/>
      <circle r="1.5" fill="{GOLD}"/>
      <path d="M0 -5 V0 H4" fill="none" stroke="{NAVY}" stroke-width="1.9" stroke-linecap="round"/>
    </g>"""


def ico_pin(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M0 -8.5 C-5.2 -8.5 -8.5 -4 -8.5 0 C-8.5 5.2 0 11.5 0 11.5 C0 11.5 8.5 5.2 8.5 0 C8.5 -4 5.2 -8.5 0 -8.5 Z" fill="{GOLD}"/>
      <circle cy="-0.3" r="2.6" fill="{WHITE}"/>
    </g>"""


def pastor(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="15" fill="{WHITE}" opacity="0.14"/>
      <circle cy="-4" r="5.2" fill="{WHITE}"/>
      <path d="M-10.5 12.5 C-10.5 4.2 -6 0.5 0 0.5 C6 0.5 10.5 4.2 10.5 12.5 Z" fill="{WHITE}"/>
    </g>"""


def phone(cx, cy):
    return f"""
    <g transform="translate({cx},{cy})">
      <rect x="-4.8" y="-8" width="9.6" height="16" rx="2" fill="none" stroke="{GOLD}" stroke-width="1.6"/>
      <circle cy="5.5" r="1" fill="{GOLD}"/>
    </g>"""


def day_premium(x, y, w, h, name, num, time_s, period):
    """Premium day block: gold number badge + icons, no heavy navy header box look."""
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WHITE}"
            stroke="{LINE}" stroke-width="1.4"/>
      <!-- left gold accent bar -->
      <path d="M{x} {y+16} Q{x} {y} {x+16} {y} L{x} {y} Z" fill="none"/>
      <rect x="{x}" y="{y}" width="7" height="{h}" rx="3" fill="{GOLD}"/>

      <!-- day name -->
      {T(x + 28, y + 28, name, size=13, fill=GOLD, weight="800", tracking="2")}

      <!-- big number circle -->
      <circle cx="{x + 52}" cy="{y + 78}" r="28" fill="{NAVY}"/>
      {T(x + 52, y + 88, str(num), size=28, fill=WHITE, weight="800", anchor="middle")}

      <!-- date label -->
      {ico_cal(x + 105, y + 68, 1.0)}
      {T(x + 122, y + 64, "Aogositra 2026", size=13, fill=NAVY, weight="700")}

      <!-- time -->
      {ico_clock(x + 105, y + 100, 1.05)}
      {T(x + 122, y + 96, time_s, size=18, fill=NAVY, weight="800")}
      {T(x + 122, y + 118, period, size=12, fill=MUTED, weight="600", family="Open Sans")}
    </g>"""


def build_svg() -> str:
    panel = ASSETS / "crowd-right-panel.jpg"
    photo = data_uri(panel)

    days = [
        ("ALAKAMISY", "6", "15:00", "3 ora tolakandro"),
        ("ZOMA", "7", "15:00", "3 ora tolakandro"),
        ("SABOTSY", "8", "15:00", "3 ora tolakandro"),
        ("ALAHADY", "9", "09:00", "9 ora maraina"),
    ]

    content_w = PHOTO_X - 50
    card_w, gap = 450, 22
    total = 4 * card_w + 3 * gap
    x0 = max(50, (content_w - total) / 2)
    cards_y = 350
    cards = "\n".join(
        day_premium(x0 + i * (card_w + gap), cards_y, card_w, 145, *d)
        for i, d in enumerate(days)
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
  <title>Fitoriana Filazantsara Lehibe — Premium</title>
  <desc>Design premium — photo mains pleine hauteur droite + dégradé</desc>

  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{IVORY}"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
    <!-- Soft fade: content dominates, photo stays BACKGROUND -->
    <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{IVORY}" stop-opacity="1"/>
      <stop offset="70%" stop-color="{IVORY}" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="{IVORY}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="photoWash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{NAVY}" stop-opacity="0.22"/>
      <stop offset="35%" stop-color="{NAVY}" stop-opacity="0.02"/>
      <stop offset="78%" stop-color="{NAVY}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{NAVY}" stop-opacity="0.40"/>
    </linearGradient>
    <!-- Rounded frame for photo panel like reference -->
    <clipPath id="rightClip">
      <path d="M{PHOTO_X + 40} 28
               Q{PHOTO_X + 40} 12 {PHOTO_X + 56} 12
               L{W - 28} 12
               Q{W - 12} 12 {W - 12} 28
               L{W - 12} {H - 28}
               Q{W - 12} {H - 12} {W - 28} {H - 12}
               L{PHOTO_X + 56} {H - 12}
               Q{PHOTO_X + 40} {H - 12} {PHOTO_X + 40} {H - 28}
               Z"/>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#pageBg)"/>

  <!-- RIGHT PHOTO as BACKGROUND (atmospheric, framed) -->
  <g clip-path="url(#rightClip)">
    <image x="{PHOTO_X + 40}" y="12" width="{PHOTO_W - 52}" height="{H - 24}"
           preserveAspectRatio="xMidYMid slice" xlink:href="{photo}" opacity="0.95"/>
    <rect x="{PHOTO_X}" y="0" width="{PHOTO_W}" height="{H}" fill="url(#photoWash)"/>
  </g>
  <!-- Soft blend — narrow so photo stays clean -->
  <rect x="{PHOTO_X - 40}" y="0" width="120" height="{H}" fill="url(#fadeL)"/>
  <!-- Navy + gold curved frame (like reference capture) -->
  <path d="M{PHOTO_X + 40} 28
           Q{PHOTO_X + 40} 12 {PHOTO_X + 56} 12
           L{W - 28} 12
           Q{W - 12} 12 {W - 12} 28
           L{W - 12} {H - 28}
           Q{W - 12} {H - 12} {W - 28} {H - 12}
           L{PHOTO_X + 56} {H - 12}
           Q{PHOTO_X + 40} {H - 12} {PHOTO_X + 40} {H - 28}
           Z"
        fill="none" stroke="{NAVY}" stroke-width="14"/>
  <path d="M{PHOTO_X + 48} 34
           Q{PHOTO_X + 48} 20 {PHOTO_X + 62} 20
           L{W - 34} 20
           Q{W - 20} 20 {W - 20} 34
           L{W - 20} {H - 34}
           Q{W - 20} {H - 20} {W - 34} {H - 20}
           L{PHOTO_X + 62} {H - 20}
           Q{PHOTO_X + 48} {H - 20} {PHOTO_X + 48} {H - 34}
           Z"
        fill="none" stroke="{GOLD}" stroke-width="2.5"/>

  <!-- TOP BAR -->
  <rect x="0" y="0" width="{PHOTO_X + 30}" height="36" fill="{NAVY}"/>
  {T(36, 24, "FIANGONANA JESOSY MPAMONJY  ·  MORAFENO AMBOSITRA",
     size=14, fill=WHITE, weight="700", tracking="3.2")}

  <!-- HEADER -->
  {logo(72, 100, 1.3)}
  <text x="145" y="88" font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="46" font-weight="800" letter-spacing="0.8">
    <tspan fill="{NAVY}">FITORIANA FILAZANTSARA </tspan>
    <tspan fill="{GOLD}">LEHIBE</tspan>
  </text>
  <text x="145" y="126" font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="15" font-weight="400" font-style="italic">
    <tspan fill="{INK}">“ Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, ka mitoria ny filazantsara amin'ny olombelona rehetra. ”</tspan>
    <tspan dx="8" fill="{GOLD}" font-style="normal" font-weight="800"
           font-family="Montserrat, DejaVu Sans, sans-serif">Marka 16:15</tspan>
  </text>
  <rect x="145" y="142" width="100" height="3" rx="1.5" fill="{GOLD}"/>

  <!-- MID -->
  {people(88, 210, 1.0)}
  {T(130, 193, "Ny Mpitandrina sy ny fiangonana", size=13.5, fill=MUTED, weight="600", family="Open Sans")}
  {T(130, 218, "JESOSY MPAMONJY MORAFENO AMBOSITRA", size=17, fill=NAVY, weight="800")}
  {T(130, 242, "dia faly manasa antsika rehetra", size=13.5, fill=MUTED, weight="600", family="Open Sans")}

  {T(860, 188, "Hanatrika ny Fitoriana Filazantsara Lehibe", size=12.5, fill=MUTED, weight="600", family="Open Sans")}
  <rect x="780" y="200" width="300" height="52" rx="12" fill="{GOLD}"/>
  {T(930, 235, "6  ·  7  ·  8  ·  9", size=28, fill=NAVY, weight="800", anchor="middle")}
  {T(1110, 235, "AOGOSITRA 2026", size=24, fill=NAVY, weight="800")}

  <!-- Benefit pills like reference -->
  <g>
    <rect x="1380" y="185" width="480" height="38" rx="10" fill="{WHITE}" stroke="{LINE}" stroke-width="1.3"/>
    {ico_flame(1405, 204)}
    {T(1430, 209, "Ho famonjena fanahin'olona", size=14, fill=NAVY, weight="700")}

    <rect x="1380" y="228" width="480" height="38" rx="10" fill="{WHITE}" stroke="{LINE}" stroke-width="1.3"/>
    {ico_star(1405, 247)}
    {T(1430, 252, "Ho fanasitranana ny aretina", size=14, fill=NAVY, weight="700")}

    <rect x="1380" y="271" width="480" height="38" rx="10" fill="{WHITE}" stroke="{LINE}" stroke-width="1.3"/>
    {ico_leaf(1405, 290)}
    {T(1430, 295, "Ho fiainana mandrakizay ho anao", size=14, fill=NAVY, weight="700")}
  </g>

  <!-- Timeline label -->
  <line x1="55" y1="295" x2="{content_w}" y2="295" stroke="{LINE}" stroke-width="1.4"/>
  {T(55, 325, "FANDAHARAM-POTOANA", size=13, fill=GOLD, weight="800", tracking="2.5")}
  {T(290, 325, "Aogositra 2026  ·  Morafeno Ambositra", size=13, fill=MUTED, weight="600", family="Open Sans")}

  <!-- Connecting gold timeline behind cards -->
  <line x1="{x0 + 60}" y1="{cards_y + 78}" x2="{x0 + total - 60}" y2="{cards_y + 78}"
        stroke="{GOLD}" stroke-width="2.5" stroke-linecap="round" opacity="0.35"/>

  {cards}

  {ico_pin(content_w/2 - 190, 515, 0.85)}
  {T(content_w/2 - 172, 520, "Fiangonana Jesosy Mpamonjy — Morafeno, Ambositra",
     size=12.5, fill=MUTED, weight="600", family="Open Sans")}

  <!-- FOOTER -->
  <rect x="0" y="545" width="{PHOTO_X + 40}" height="155" fill="{NAVY}"/>
  <rect x="0" y="545" width="{PHOTO_X + 40}" height="4" fill="{GOLD}"/>

  {T(50, 595, "Anasana antsika rehetra — tongava handray ny anjaranao!",
     size=21, fill=GOLD, family="Dancing Script", weight="700")}
  {T(50, 628, "Fotoana lehibe ho an'ny fanahy, ny fanasitranana ary ny fiainana mandrakizay.",
     size=12.5, fill="#9AADC4", weight="500", family="Open Sans")}

  <rect x="1050" y="568" width="760" height="110" rx="12" fill="{NAVY_MID}"/>
  <rect x="1050" y="568" width="5" height="110" fill="{GOLD}"/>
  {pastor(1105, 623, 1.15)}
  {T(1145, 598, "Ny Mpitandrina", size=12, fill=GOLD, weight="600")}
  {T(1145, 626, "RANDRIANARIZANANY Lovasoa Fenomanana", size=15.5, fill=WHITE, weight="700")}
  {phone(1155, 655)}
  {T(1180, 660, "038 92 546 27  ·  033 20 968 28", size=14.5, fill=WHITE, weight="600")}

  {T(W - 55, 660, "Tongava!", size=26, fill=WHITE, weight="400",
     family="Dancing Script", anchor="end")}
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
        raise RuntimeError(r.stderr[-1500:])
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
    print(f"Wrote {svg} ({svg.stat().st_size/1e6:.2f} MB)")

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
