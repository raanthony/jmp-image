#!/usr/bin/env python3
"""
Banderole premium 3,00 × 0,70 m
- Contenu gauche ~80 %, fond droit ~20 %
- Textes / icônes agrandis, peu d'espace vide
- Bande haute pleine largeur, texte centré
- Bénéfices sur le fond + pied Mpitandrina débordant
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
NAVY_MID = "#0C2D55"
GOLD = "#C97B14"
ORANGE = "#E08A1A"
WHITE = "#FFFFFF"
IVORY = "#FFFCFA"
MUTED = "#667384"
INK = "#1A2430"
LINE = "#DDE3EC"
GREEN = "#278A3D"
BLUE = "#1B6CA8"

W, H = 3000, 700
# Right atmospheric panel ≈ 20 % of width (left content ≈ 80 %)
PHOTO_X = 2380
PHOTO_W = W - PHOTO_X  # 620
FADE_W = 320


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
      <path d="M-32 17 C-20 9.5 -8 9.5 0 13.5 C8 9.5 20 9.5 32 17 L32 25.5 C20 18 8 18 0 22 C-8 18 -20 18 -32 25.5 Z" fill="{NAVY}"/>
      <path d="M-27 17 C-16 12 -7 12 0 14.8 C7 12 16 12 27 17" fill="none" stroke="{GOLD}" stroke-width="2"/>
      <path d="M-22 -8 L-22 11 L22 11 L22 -8 L0 -29 Z" fill="{NAVY}"/>
      <path d="M-28 -6 L0 -33 L28 -6" fill="none" stroke="{GOLD}" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>
      <rect x="-5.5" y="-1" width="11" height="12" rx="1.1" fill="{GOLD}"/>
      <circle cx="-10" cy="-11" r="3.5" fill="{GOLD}"/>
      <circle cx="0" cy="-13.5" r="4.2" fill="{ORANGE}"/>
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
      <path d="M-15.5 12.5 C-15.5 5.5 -12.5 1 -8.5 1 C-4.5 1 -2.8 4.5 -2.3 8.5" fill="{GOLD}"/>
      <path d="M-7 14 C-7 4.5 -3.5 -1 0 -1 C3.5 -1 7 4.5 7 14 Z" fill="{ORANGE}"/>
      <path d="M2.3 8.5 C2.8 4.5 4.5 1 8.5 1 C12.5 1 15.5 5.5 15.5 12.5" fill="{GOLD}"/>
    </g>"""


def ico_flame(cx, cy, r=14):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GOLD}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.08} {-r*0.4} {-r*0.3} {-r*0.12} {-r*0.68}
               C{-r*0.02} {-r*0.22} {r*0.18} {-r*0.38} {r*0.22} {-r*0.72}
               C{r*0.58} {-r*0.22} {r*0.52} {r*0.22} 0 {r*0.55} Z" fill="{WHITE}"/>
    </g>"""


def ico_star(cx, cy, r=14):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{BLUE}"/>
      <path d="M0 {-r*0.55} L{r*0.15} {-r*0.14} L{r*0.55} {-r*0.14} L{r*0.22} {r*0.12}
               L{r*0.34} {r*0.52} L0 {r*0.26} L{-r*0.34} {r*0.52} L{-r*0.22} {r*0.12}
               L{-r*0.55} {-r*0.14} L{-r*0.15} {-r*0.14} Z" fill="{WHITE}"/>
    </g>"""


def ico_leaf(cx, cy, r=14):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GREEN}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.08} {-r*0.5} {-r*0.4} 0 {-r*0.65}
               C{r*0.5} {-r*0.4} {r*0.5} {r*0.08} 0 {r*0.55} Z" fill="{WHITE}"/>
      <path d="M0 {r*0.42} V{-r*0.55}" stroke="{GREEN}" stroke-width="1.3"/>
    </g>"""


def ico_cal_grid(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <rect x="-9" y="-8" width="18" height="16" rx="2.2" fill="none" stroke="{NAVY}" stroke-width="1.8"/>
      <line x1="-9" y1="-2.5" x2="9" y2="-2.5" stroke="{NAVY}" stroke-width="1.5"/>
      <line x1="-3" y1="-8" x2="-3" y2="8" stroke="{NAVY}" stroke-width="1.1"/>
      <line x1="3" y1="-8" x2="3" y2="8" stroke="{NAVY}" stroke-width="1.1"/>
      <line x1="-9" y1="2.8" x2="9" y2="2.8" stroke="{NAVY}" stroke-width="1.1"/>
    </g>"""


def ico_pin(cx, cy, s=1.0, fill=GOLD):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M0 -9 C-5.5 -9 -9 -4.5 -9 0 C-9 5.5 0 12 0 12 C0 12 9 5.5 9 0 C9 -4.5 5.5 -9 0 -9 Z" fill="{fill}"/>
      <circle cy="-0.5" r="2.6" fill="{WHITE}"/>
    </g>"""


def ico_phone(cx, cy, fill=GOLD, s=1.15):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <rect x="-5" y="-8.5" width="10" height="17" rx="2.2" fill="none" stroke="{fill}" stroke-width="1.6"/>
      <circle cy="5.8" r="1.1" fill="{fill}"/>
    </g>"""


def pastor_gold(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="28" fill="{GOLD}"/>
      <circle cy="-6" r="9" fill="{WHITE}"/>
      <path d="M-18 22 C-18 8 -10 2 0 2 C10 2 18 8 18 22 Z" fill="{WHITE}"/>
    </g>"""


def wheat(cx, cy, flip=False, s=1.0):
    sx = -s if flip else s
    return f"""
    <g transform="translate({cx},{cy}) scale({sx},{s})" fill="{GOLD}">
      <path d="M0 1 C14 -10 30 -12 44 -8 C30 -4 16 0 0 1 Z" opacity="0.95"/>
      <path d="M5 0 C18 -15 36 -20 52 -14 C36 -10 20 -2 5 0 Z" opacity="0.7"/>
      <path d="M10 5 C24 -2 40 -2 54 4 C40 7 26 10 10 5 Z" opacity="0.85"/>
    </g>"""


def benefit_on_bg(x, y, w, icon_fn, label):
    """White pill on the narrow right panel — larger type."""
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="58" rx="29" fill="{WHITE}" opacity="0.97"/>
      {icon_fn(x + 30, y + 29, 15)}
      {T(x + 54, y + 37, label, size=14.5, fill=NAVY, weight="700")}
    </g>"""


def day_row_item(x, y, w, num, place):
    """Larger timeline item: calendar + number + pin + place."""
    return f"""
    <g>
      {ico_cal_grid(x + 28, y + 22, 1.45)}
      {T(x + 52, y + 34, str(num), size=48, fill=NAVY, weight="800")}
      {T(x + 52, y + 58, "Aogositra", size=14, fill=MUTED, weight="600", family="Open Sans")}
      {ico_pin(x + 145, y + 26, 1.15, fill=BLUE)}
      {T(x + 162, y + 20, place[0], size=15, fill=INK, weight="600", family="Open Sans")}
      {T(x + 162, y + 42, place[1], size=15, fill=MUTED, weight="700", family="Open Sans")}
      {T(x + 162, y + 62, place[2] if len(place) > 2 else "", size=14, fill=MUTED, weight="500", family="Open Sans")}
    </g>"""


def build_svg() -> str:
    panel = ASSETS / "crowd-right-panel.jpg"
    photo = data_uri(panel)

    places = [
        ["ao @ Fiangonana", "JESOSY MPAMONJY", "Morafeno"],
        ["ao @ Fiangonana", "JESOSY MPAMONJY", "Morafeno"],
        ["ao @ Fiangonana", "JESOSY MPAMONJY", "Morafeno"],
        ["ao @ Fiangonana", "JESOSY MPAMONJY", "Morafeno"],
    ]
    day_nums = ["6", "7", "8", "9"]
    day_names = ["ALAKAMISY", "ZOMA", "SABOTSY", "ALAHADY"]
    day_times = [
        "15:00  ·  tolakandro",
        "15:00  ·  tolakandro",
        "15:00  ·  tolakandro",
        "09:00  ·  maraina",
    ]
    # Fill left ~80 % — timeline spans almost to photo fade
    content_right = PHOTO_X - 40
    x0 = 40
    gap = 22
    item_w = (content_right - x0 - 3 * gap) / 4
    timeline_y = 448
    items = []
    for i, (num, place) in enumerate(zip(day_nums, places)):
        xi = x0 + i * (item_w + gap)
        items.append(day_row_item(xi, timeline_y, item_w, num, place))
        if i < 3:
            items.append(
                f'<line x1="{xi + item_w + gap/2}" y1="{timeline_y + 4}" '
                f'x2="{xi + item_w + gap/2}" y2="{timeline_y + 72}" '
                f'stroke="{LINE}" stroke-width="1.8"/>'
            )
    timeline = "\n".join(items)

    # Benefits on narrow right panel
    bx = PHOTO_X + 24
    bw = PHOTO_W - 44
    benefits = "\n".join([
        benefit_on_bg(bx, 55, bw, ico_flame, "Ho famonjena fanahin'olona"),
        benefit_on_bg(bx, 130, bw, ico_star, "Ho fanasitranana ny aretina"),
        benefit_on_bg(bx, 205, bw, ico_leaf, "Ho fiainana mandrakizay ho anao"),
    ])

    foot_y = 605
    foot_h = H - foot_y
    pastor_x, pastor_y = 2120, 488
    pastor_w, pastor_h = 850, 195
    r_tl = 54

    day_labels = []
    for i, (name, time_s) in enumerate(zip(day_names, day_times)):
        xi = x0 + i * (item_w + gap)
        day_labels.append(T(xi + 52, 382, name, size=17, fill=GOLD, weight="800", tracking="1.2"))
        day_labels.append(T(xi + 52, 410, time_s, size=16, fill=MUTED, weight="600", family="Open Sans"))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
  <title>Fitoriana Filazantsara Lehibe — Premium</title>
  <desc>Contenu large, fond droit 20%, bande haute pleine largeur</desc>

  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{IVORY}"/>
      <stop offset="70%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FFF6EC"/>
    </linearGradient>
    <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="22%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="78%" stop-color="#FFF8F0" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#pageBg)"/>

  <!-- ===== RIGHT BACKGROUND (~20 %) ===== -->
  <image x="{PHOTO_X}" y="0" width="{PHOTO_W}" height="{H}"
         preserveAspectRatio="xMidYMid slice" xlink:href="{photo}" opacity="0.92"/>
  <rect x="{PHOTO_X - 80}" y="0" width="{FADE_W}" height="{H}" fill="url(#fadeL)"/>

  {benefits}

  <!-- ===== TOP BAR — full width, centered ===== -->
  <rect x="0" y="0" width="{W}" height="46" fill="{NAVY}"/>
  {T(W/2, 31, "FIANGONANA JESOSY MPAMONJY  ·  MORAFENO AMBOSITRA",
     size=18, fill=WHITE, weight="700", tracking="5", anchor="middle")}

  <!-- ===== HEADER (larger, fills left zone) ===== -->
  {logo(92, 125, 1.8)}
  <text x="185" y="112" font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="58" font-weight="800" letter-spacing="1">
    <tspan fill="{NAVY}">FITORIANA FILAZANTSARA </tspan>
    <tspan fill="{GOLD}">LEHIBE</tspan>
  </text>
  <text x="185" y="158" font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="19" font-weight="400" font-style="italic">
    <tspan fill="{INK}">“ Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, ka mitoria ny filazantsara amin'ny olombelona rehetra. ”</tspan>
    <tspan dx="12" fill="{GOLD}" font-style="normal" font-weight="800"
           font-family="Montserrat, DejaVu Sans, sans-serif" font-size="19">Marka 16:15</tspan>
  </text>
  <rect x="185" y="174" width="120" height="4.5" rx="2" fill="{GOLD}"/>

  <!-- ===== INVITE + DATES (spread across left 80 %) ===== -->
  {people(100, 245, 1.35)}
  {T(162, 222, "Ny Mpitandrina sy ny fiangonana", size=18, fill=MUTED, weight="600", family="Open Sans")}
  {T(162, 254, "JESOSY MPAMONJY MORAFENO AMBOSITRA", size=24, fill=NAVY, weight="800")}
  {T(162, 286, "dia faly manasa antsika rehetra", size=18, fill=MUTED, weight="600", family="Open Sans")}

  {T(1320, 222, "Hanatrika ny Fitoriana Filazantsara Lehibe", size=17, fill=MUTED, weight="600", family="Open Sans")}
  <rect x="1240" y="240" width="380" height="64" rx="15" fill="{GOLD}"/>
  {T(1430, 282, "6  ·  7  ·  8  ·  9", size=34, fill=NAVY, weight="800", anchor="middle")}
  {T(1660, 282, "AOGOSITRA 2026", size=30, fill=NAVY, weight="800")}

  <!-- ===== TIMELINE ===== -->
  <line x1="40" y1="318" x2="{content_right}" y2="318" stroke="{LINE}" stroke-width="1.8"/>
  {T(40, 355, "FANDAHARAM-POTOANA", size=18, fill=GOLD, weight="800", tracking="2.5")}
  {T(360, 355, "Aogositra 2026  ·  Morafeno Ambositra", size=17, fill=MUTED, weight="600", family="Open Sans")}

  {''.join(day_labels)}
  {timeline}

  <!-- ===== FOOTER ===== -->
  <rect x="0" y="{foot_y}" width="{W}" height="{foot_h}" fill="{NAVY}"/>
  <rect x="0" y="{foot_y}" width="{W}" height="3" fill="{GOLD}"/>

  {wheat(28, foot_y + 54, False, 1.2)}
  <text x="120" y="{foot_y + 60}" font-family="Great Vibes, Dancing Script, DejaVu Sans, sans-serif"
        font-size="42" font-weight="400">
    <tspan fill="{WHITE}">Anasana antsika rehetra hanatrika izany fotoana lehibe izany, </tspan>
    <tspan fill="{GOLD}">tongava handray ny anjaranao!</tspan>
  </text>
  {wheat(pastor_x - 55, foot_y + 54, True, 1.2)}

  <!-- ===== MPITANDRINA — overflow + rounded TL ===== -->
  <path d="M{pastor_x} {pastor_y + r_tl}
           Q{pastor_x} {pastor_y} {pastor_x + r_tl} {pastor_y}
           L{pastor_x + pastor_w} {pastor_y}
           L{pastor_x + pastor_w} {pastor_y + pastor_h}
           L{pastor_x} {pastor_y + pastor_h}
           Z" fill="{NAVY}"/>
  <path d="M{pastor_x} {pastor_y + r_tl}
           Q{pastor_x} {pastor_y} {pastor_x + r_tl} {pastor_y}
           L{pastor_x + r_tl + 5} {pastor_y}
           L{pastor_x + 5} {pastor_y + r_tl}
           L{pastor_x + 5} {pastor_y + pastor_h}
           L{pastor_x} {pastor_y + pastor_h}
           Z" fill="{GOLD}"/>
  <path d="M{pastor_x + pastor_w - 42} {pastor_y + 20}
           l3.2 8 8.5 1 -6.2 5.5 1.8 8.5 -7.3 -4 -7.3 4 1.8 -8.5 -6.2 -5.5 8.5 -1 z"
        fill="{WHITE}" opacity="0.22"/>

  {pastor_gold(pastor_x + 72, pastor_y + 90, 1.1)}
  {T(pastor_x + 118, pastor_y + 55, "Ny Mpitandrina:", size=14, fill=GOLD, weight="600")}
  {T(pastor_x + 118, pastor_y + 90, "RANDRIANARIZANANY", size=24, fill=WHITE, weight="800")}
  {T(pastor_x + 118, pastor_y + 118, "Lovasoa Fenomanana", size=16, fill=WHITE, weight="500", family="Open Sans")}
  {ico_phone(pastor_x + 132, pastor_y + 152)}
  {T(pastor_x + 152, pastor_y + 157, "Tel : 038 92 546 27  /  033 20 968 28", size=15, fill=WHITE, weight="600")}
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
