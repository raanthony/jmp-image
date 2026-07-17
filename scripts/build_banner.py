#!/usr/bin/env python3
"""
Banderole premium 3,00 × 0,70 m
- Fond atmosphérique à droite (fondu doux, en arrière-plan)
- Bénéfices superposés sur le fond
- Pied compact + CTA une ligne
- Bloc Mpitandrina débordant, coin haut-gauche arrondi
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
# Photo starts earlier; SVG fade does the soft blend (no hard cut)
PHOTO_X = 1380
PHOTO_W = W - PHOTO_X
FADE_W = 780


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


def ico_flame(cx, cy, r=12):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GOLD}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.08} {-r*0.4} {-r*0.3} {-r*0.12} {-r*0.68}
               C{-r*0.02} {-r*0.22} {r*0.18} {-r*0.38} {r*0.22} {-r*0.72}
               C{r*0.58} {-r*0.22} {r*0.52} {r*0.22} 0 {r*0.55} Z" fill="{WHITE}"/>
    </g>"""


def ico_star(cx, cy, r=12):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{BLUE}"/>
      <path d="M0 {-r*0.55} L{r*0.15} {-r*0.14} L{r*0.55} {-r*0.14} L{r*0.22} {r*0.12}
               L{r*0.34} {r*0.52} L0 {r*0.26} L{-r*0.34} {r*0.52} L{-r*0.22} {r*0.12}
               L{-r*0.55} {-r*0.14} L{-r*0.15} {-r*0.14} Z" fill="{WHITE}"/>
    </g>"""


def ico_leaf(cx, cy, r=12):
    return f"""
    <g transform="translate({cx},{cy})">
      <circle r="{r}" fill="{GREEN}"/>
      <path d="M0 {r*0.55} C{-r*0.5} {r*0.08} {-r*0.5} {-r*0.4} 0 {-r*0.65}
               C{r*0.5} {-r*0.4} {r*0.5} {r*0.08} 0 {r*0.55} Z" fill="{WHITE}"/>
      <path d="M0 {r*0.42} V{-r*0.55}" stroke="{GREEN}" stroke-width="1.2"/>
    </g>"""


def ico_cal_grid(cx, cy, s=1.0):
    """Small calendar grid icon like capture."""
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <rect x="-8" y="-7" width="16" height="14" rx="2" fill="none" stroke="{NAVY}" stroke-width="1.6"/>
      <line x1="-8" y1="-2" x2="8" y2="-2" stroke="{NAVY}" stroke-width="1.4"/>
      <line x1="-2.5" y1="-7" x2="-2.5" y2="7" stroke="{NAVY}" stroke-width="1"/>
      <line x1="2.5" y1="-7" x2="2.5" y2="7" stroke="{NAVY}" stroke-width="1"/>
      <line x1="-8" y1="2.5" x2="8" y2="2.5" stroke="{NAVY}" stroke-width="1"/>
    </g>"""


def ico_pin(cx, cy, s=1.0, fill=GOLD):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M0 -8 C-5 -8 -8 -4 -8 0 C-8 5 0 11 0 11 C0 11 8 5 8 0 C8 -4 5 -8 0 -8 Z" fill="{fill}"/>
      <circle cy="-0.5" r="2.4" fill="{WHITE}"/>
    </g>"""


def ico_phone(cx, cy, fill=GOLD):
    return f"""
    <g transform="translate({cx},{cy})">
      <rect x="-4.5" y="-7.5" width="9" height="15" rx="2" fill="none" stroke="{fill}" stroke-width="1.5"/>
      <circle cy="5.2" r="1" fill="{fill}"/>
    </g>"""


def pastor_gold(cx, cy, s=1.0):
    """Gold circle with white silhouette — like capture."""
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="28" fill="{GOLD}"/>
      <circle cy="-6" r="9" fill="{WHITE}"/>
      <path d="M-18 22 C-18 8 -10 2 0 2 C10 2 18 8 18 22 Z" fill="{WHITE}"/>
    </g>"""


def wheat(cx, cy, flip=False):
    sx = -1 if flip else 1
    return f"""
    <g transform="translate({cx},{cy}) scale({sx},1)" fill="{GOLD}">
      <path d="M0 1 C14 -10 30 -12 44 -8 C30 -4 16 0 0 1 Z" opacity="0.95"/>
      <path d="M5 0 C18 -15 36 -20 52 -14 C36 -10 20 -2 5 0 Z" opacity="0.7"/>
      <path d="M10 5 C24 -2 40 -2 54 4 C40 7 26 10 10 5 Z" opacity="0.85"/>
    </g>"""


def benefit_on_bg(x, y, w, icon_fn, label):
    """White pill sitting clearly above the background."""
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="46" rx="23" fill="{WHITE}" opacity="0.96"/>
      {icon_fn(x + 26, y + 23)}
      {T(x + 48, y + 30, label, size=15.5, fill=NAVY, weight="700")}
    </g>"""


def day_row_item(x, y, w, num, place):
    """Timeline item like capture: calendar icon + big number + pin + place."""
    return f"""
    <g>
      {ico_cal_grid(x + 22, y + 18, 1.15)}
      {T(x + 42, y + 28, str(num), size=36, fill=NAVY, weight="800")}
      {T(x + 42, y + 48, "Aogositra", size=11, fill=MUTED, weight="600", family="Open Sans")}
      {ico_pin(x + 110, y + 22, 0.85, fill=BLUE)}
      {T(x + 124, y + 18, place[0], size=11.5, fill=INK, weight="600", family="Open Sans")}
      {T(x + 124, y + 36, place[1], size=11.5, fill=MUTED, weight="600", family="Open Sans")}
      {T(x + 124, y + 52, place[2] if len(place) > 2 else "", size=11, fill=MUTED, weight="500", family="Open Sans")}
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
    # Compact timeline row (sits above slim footer)
    day_nums = ["6", "7", "8", "9"]
    item_w = 365
    gap = 14
    total = 4 * item_w + 3 * gap
    x0 = 40
    timeline_y = 400
    items = []
    for i, (num, place) in enumerate(zip(day_nums, places)):
        xi = x0 + i * (item_w + gap)
        items.append(day_row_item(xi, timeline_y, item_w, num, place))
        if i < 3:
            items.append(
                f'<line x1="{xi + item_w + gap/2}" y1="{timeline_y}" '
                f'x2="{xi + item_w + gap/2}" y2="{timeline_y + 60}" '
                f'stroke="{LINE}" stroke-width="1.5"/>'
            )
    timeline = "\n".join(items)

    # Benefits clearly ON the visible photo (right of soft fade zone)
    bx = PHOTO_X + int(FADE_W * 0.72)
    benefits = "\n".join([
        benefit_on_bg(bx, 52, 540, ico_flame, "Ho famonjena fanahin'olona"),
        benefit_on_bg(bx, 112, 540, ico_star, "Ho fanasitranana ny aretina"),
        benefit_on_bg(bx, 172, 540, ico_leaf, "Ho fiainana mandrakizay ho anao"),
    ])

    # Slim footer; pastor tab overlaps upward with rounded TL
    foot_y = 618
    foot_h = H - foot_y  # ~82
    pastor_x, pastor_y = 2010, 510
    pastor_w, pastor_h = 960, 175
    r_tl = 58  # large rounded top-left like capture

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
  <title>Fitoriana Filazantsara Lehibe — Premium</title>
  <desc>Fond fondu + bénéfices dessus + pied Mpitandrina débordant</desc>

  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{IVORY}"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FFF6EC"/>
    </linearGradient>
    <!-- Ultra-wide soft blend into photo -->
    <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="15%" stop-color="#FFFFFF" stop-opacity="0.98"/>
      <stop offset="35%" stop-color="#FFFFFF" stop-opacity="0.82"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.52"/>
      <stop offset="75%" stop-color="#FFF9F2" stop-opacity="0.22"/>
      <stop offset="90%" stop-color="#FFF6EC" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#pageBg)"/>

  <!-- ===== RIGHT BACKGROUND (soft, behind content) ===== -->
  <image x="{PHOTO_X}" y="0" width="{PHOTO_W}" height="{H}"
         preserveAspectRatio="xMidYMid slice" xlink:href="{photo}" opacity="0.9"/>
  <!-- Wide soft fade into left white — no hard cut, no grey veil -->
  <rect x="{PHOTO_X - 40}" y="0" width="{FADE_W}" height="{H}" fill="url(#fadeL)"/>

  <!-- Benefits ON TOP of background -->
  {benefits}

  <!-- ===== TOP BAR ===== -->
  <rect x="0" y="0" width="{PHOTO_X + 40}" height="34" fill="{NAVY}"/>
  {T(32, 23, "FIANGONANA JESOSY MPAMONJY  ·  MORAFENO AMBOSITRA",
     size=13.5, fill=WHITE, weight="700", tracking="3")}

  <!-- ===== HEADER ===== -->
  {logo(68, 95, 1.25)}
  <text x="140" y="82" font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="42" font-weight="800" letter-spacing="0.6">
    <tspan fill="{NAVY}">FITORIANA FILAZANTSARA </tspan>
    <tspan fill="{GOLD}">LEHIBE</tspan>
  </text>
  <text x="140" y="118" font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="14" font-weight="400" font-style="italic">
    <tspan fill="{INK}">“ Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, ka mitoria ny filazantsara amin'ny olombelona rehetra. ”</tspan>
    <tspan dx="8" fill="{GOLD}" font-style="normal" font-weight="800"
           font-family="Montserrat, DejaVu Sans, sans-serif">Marka 16:15</tspan>
  </text>
  <rect x="140" y="132" width="90" height="3" rx="1.5" fill="{GOLD}"/>

  <!-- ===== INVITE + DATES ===== -->
  {people(82, 195, 0.95)}
  {T(125, 178, "Ny Mpitandrina sy ny fiangonana", size=13, fill=MUTED, weight="600", family="Open Sans")}
  {T(125, 202, "JESOSY MPAMONJY MORAFENO AMBOSITRA", size=16, fill=NAVY, weight="800")}
  {T(125, 224, "dia faly manasa antsika rehetra", size=13, fill=MUTED, weight="600", family="Open Sans")}

  {T(780, 175, "Hanatrika ny Fitoriana Filazantsara Lehibe", size=12, fill=MUTED, weight="600", family="Open Sans")}
  <rect x="720" y="188" width="280" height="48" rx="11" fill="{GOLD}"/>
  {T(860, 220, "6  ·  7  ·  8  ·  9", size=26, fill=NAVY, weight="800", anchor="middle")}
  {T(1030, 220, "AOGOSITRA 2026", size=22, fill=NAVY, weight="800")}

  <!-- ===== TIMELINE (compact, like capture) ===== -->
  <line x1="40" y1="268" x2="1550" y2="268" stroke="{LINE}" stroke-width="1.3"/>
  {T(40, 298, "FANDAHARAM-POTOANA", size=12, fill=GOLD, weight="800", tracking="2")}
  {T(260, 298, "Aogositra 2026  ·  Morafeno Ambositra", size=12, fill=MUTED, weight="600", family="Open Sans")}

  <!-- Day names row -->
  {T(x0 + 42, 348, "ALAKAMISY", size=12, fill=GOLD, weight="800", tracking="1")}
  {T(x0 + item_w + gap + 42, 348, "ZOMA", size=12, fill=GOLD, weight="800", tracking="1")}
  {T(x0 + 2*(item_w+gap) + 42, 348, "SABOTSY", size=12, fill=GOLD, weight="800", tracking="1")}
  {T(x0 + 3*(item_w+gap) + 42, 348, "ALAHADY", size=12, fill=GOLD, weight="800", tracking="1")}

  <!-- Times under names -->
  {T(x0 + 42, 372, "15:00  ·  tolakandro", size=12, fill=MUTED, weight="600", family="Open Sans")}
  {T(x0 + item_w + gap + 42, 372, "15:00  ·  tolakandro", size=12, fill=MUTED, weight="600", family="Open Sans")}
  {T(x0 + 2*(item_w+gap) + 42, 372, "15:00  ·  tolakandro", size=12, fill=MUTED, weight="600", family="Open Sans")}
  {T(x0 + 3*(item_w+gap) + 42, 372, "09:00  ·  maraina", size=12, fill=MUTED, weight="600", family="Open Sans")}

  {timeline}

  <!-- ===== SLIM FOOTER ===== -->
  <rect x="0" y="{foot_y}" width="{W}" height="{foot_h}" fill="{NAVY}"/>
  <rect x="0" y="{foot_y}" width="{W}" height="2.5" fill="{GOLD}"/>

  <!-- CTA: large script, single line (fits left of pastor block) -->
  {wheat(24, foot_y + 48, False)}
  <text x="110" y="{foot_y + 54}" font-family="Great Vibes, Dancing Script, DejaVu Sans, sans-serif"
        font-size="36" font-weight="400">
    <tspan fill="{WHITE}">Anasana antsika rehetra hanatrika izany fotoana lehibe izany, </tspan>
    <tspan fill="{GOLD}">tongava handray ny anjaranao!</tspan>
  </text>
  {wheat(pastor_x - 55, foot_y + 48, True)}

  <!-- ===== MPITANDRINA — overflows footer, big rounded top-left ===== -->
  <path d="M{pastor_x} {pastor_y + r_tl}
           Q{pastor_x} {pastor_y} {pastor_x + r_tl} {pastor_y}
           L{pastor_x + pastor_w} {pastor_y}
           L{pastor_x + pastor_w} {pastor_y + pastor_h}
           L{pastor_x} {pastor_y + pastor_h}
           Z" fill="{NAVY}"/>
  <!-- gold edge along rounded TL + left side -->
  <path d="M{pastor_x} {pastor_y + r_tl}
           Q{pastor_x} {pastor_y} {pastor_x + r_tl} {pastor_y}
           L{pastor_x + r_tl + 5} {pastor_y}
           L{pastor_x + 5} {pastor_y + r_tl}
           L{pastor_x + 5} {pastor_y + pastor_h}
           L{pastor_x} {pastor_y + pastor_h}
           Z" fill="{GOLD}"/>
  <path d="M{pastor_x + pastor_w - 48} {pastor_y + 22}
           l3.5 9 9.5 1 -7 6 2 9.5 -8 -4.5 -8 4.5 2 -9.5 -7 -6 9.5 -1 z"
        fill="{WHITE}" opacity="0.22"/>

  {pastor_gold(pastor_x + 78, pastor_y + 88, 1.05)}
  {T(pastor_x + 128, pastor_y + 55, "Ny Mpitandrina:", size=13, fill=GOLD, weight="600")}
  {T(pastor_x + 128, pastor_y + 88, "RANDRIANARIZANANY", size=24, fill=WHITE, weight="800")}
  {T(pastor_x + 128, pastor_y + 114, "Lovasoa Fenomanana", size=15, fill=WHITE, weight="500", family="Open Sans")}
  {ico_phone(pastor_x + 140, pastor_y + 148)}
  {T(pastor_x + 158, pastor_y + 153, "Tel : 038 92 546 27  /  033 20 968 28", size=14, fill=WHITE, weight="600")}
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
