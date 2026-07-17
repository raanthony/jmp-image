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
# Right panel ~20 %; ultra-wide soft fade into left
PHOTO_X = 2280
PHOTO_W = W - PHOTO_X
FADE_W = 680


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
    """House/community logo — embedded PNG from capture-matched asset."""
    uri = data_uri(ASSETS / "logo-maison.png")
    # native art ~76 wide in design units at s=1; PNG drawn at 76*s
    w = 78 * s
    return f"""
    <image x="{cx - w/2}" y="{cy - w/2 - 4}" width="{w}" height="{w}"
           preserveAspectRatio="xMidYMid meet" xlink:href="{uri}"/>"""


def people(cx, cy, s=1.0):
    """Community care circle — embedded PNG from capture-matched asset."""
    uri = data_uri(ASSETS / "icon-communaute.png")
    w = 52 * s
    return f"""
    <image x="{cx - w/2}" y="{cy - w/2}" width="{w}" height="{w}"
           preserveAspectRatio="xMidYMid meet" xlink:href="{uri}"/>"""


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


def ico_book(cx, cy, s=1.0, fill=GOLD):
    """Recognizable open-book icon before Marka reference."""
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M0 -8 L-11 -8 C-13.5 -8 -15 -6.5 -15 -4.5 V7.5 C-15 9 -13.5 10 -12 9.5
               L0 6.5 L12 9.5 C13.5 10 15 9 15 7.5 V-4.5 C15 -6.5 13.5 -8 11 -8 Z" fill="{fill}"/>
      <path d="M0 -8 V6.5" stroke="{NAVY}" stroke-width="1.4" opacity="0.45"/>
      <path d="M-11 -4.5 H-3 M-11 -1 H-3 M-11 2.2 H-3" stroke="{WHITE}" stroke-width="1.1" opacity="0.85"/>
      <path d="M3 -4.5 H11 M3 -1 H11 M3 2.2 H11" stroke="{WHITE}" stroke-width="1.1" opacity="0.85"/>
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
      <circle r="26" fill="{GOLD}"/>
      <circle cy="-5.5" r="8.2" fill="{WHITE}"/>
      <path d="M-16.5 20 C-16.5 7.5 -9.5 2 0 2 C9.5 2 16.5 7.5 16.5 20 Z" fill="{WHITE}"/>
    </g>"""


def burst(cx, cy, flip=False, s=1.0):
    """Gold announcement splash inspired by reference (vector, not copied)."""
    sx = -s if flip else s
    return f"""
    <g transform="translate({cx},{cy}) scale({sx},{s})" fill="{GOLD}">
      <path d="M-14 -18 C-10 -18 -8 -10 -8 -2 C-8 6 -10 14 -14 16 C-16 10 -17 2 -17 -2
               C-17 -10 -16 -18 -14 -18 Z" opacity="0.5"/>
      <ellipse cx="-12.5" cy="-4" rx="4.2" ry="12" opacity="0.85"/>
      <circle cx="-12.5" cy="14" r="2.6" opacity="0.9"/>
      <path d="M0 -4 C14 -18 32 -22 50 -16 C34 -12 16 -6 0 -4 Z" opacity="0.95"/>
      <path d="M0 -1 C18 -10 40 -12 58 -6 C40 -4 18 1 0 -1 Z" opacity="1"/>
      <path d="M0 2 C16 0 36 2 52 8 C36 6 16 5 0 2 Z" opacity="0.92"/>
      <path d="M1 5 C14 8 30 14 46 18 C30 12 14 8 1 5 Z" opacity="0.8"/>
      <path d="M2 8 C12 14 24 20 38 24 C24 18 12 12 2 8 Z" opacity="0.65"/>
      <circle cx="1" cy="1" r="3.8" opacity="1"/>
    </g>"""


def benefit_on_bg(x, y, w, icon_fn, label):
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="56" rx="28" fill="{WHITE}" opacity="0.97"/>
      {icon_fn(x + 30, y + 28, 15)}
      {T(x + 54, y + 36, label, size=15.5, fill=NAVY, weight="700")}
    </g>"""


def day_row_item(x, y, w, num, place):
    """Premium timeline column — larger type, clear hierarchy."""
    cx = x + w / 2
    return f"""
    <g>
      {ico_cal_grid(cx - 100, y + 28, 1.8)}
      {T(cx - 70, y + 42, str(num), size=58, fill=NAVY, weight="800")}
      {T(cx - 70, y + 68, "Aogositra", size=16, fill=MUTED, weight="600", family="Open Sans")}
      {ico_pin(cx + 18, y + 30, 1.4, fill=BLUE)}
      {T(cx + 40, y + 24, place[0], size=17, fill=INK, weight="600", family="Open Sans")}
      {T(cx + 40, y + 48, place[1], size=17, fill=NAVY, weight="800", family="Open Sans")}
      {T(cx + 40, y + 70, place[2] if len(place) > 2 else "", size=16, fill=MUTED, weight="600", family="Open Sans")}
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

    # Left content zone — center title / quote / invite / schedule here
    left_x0 = 50
    content_right = PHOTO_X - 80
    left_w = content_right - left_x0
    left_cx = left_x0 + left_w / 2

    x0 = left_x0
    gap = 16
    item_w = (content_right - x0 - 3 * gap) / 4
    timeline_y = 480
    items = []
    for i, (num, place) in enumerate(zip(day_nums, places)):
        xi = x0 + i * (item_w + gap)
        items.append(day_row_item(xi, timeline_y, item_w, num, place))
        if i < 3:
            items.append(
                f'<line x1="{xi + item_w + gap/2}" y1="{timeline_y}" '
                f'x2="{xi + item_w + gap/2}" y2="{timeline_y + 78}" '
                f'stroke="{LINE}" stroke-width="1.8"/>'
            )
    timeline = "\n".join(items)

    # Pastor flush right — narrower & shorter
    foot_y = 612
    foot_h = H - foot_y
    pastor_w, pastor_h = 640, 145
    pastor_x = W - pastor_w
    pastor_y = 542
    r_tl = 42

    bx = PHOTO_X + 28
    bw = PHOTO_W - 48
    pill_h, pill_gap, n_pills = 56, 18, 3
    stack_h = n_pills * pill_h + (n_pills - 1) * pill_gap
    zone_top, zone_bot = 52, pastor_y - 14
    ben_y0 = zone_top + max(0, (zone_bot - zone_top - stack_h) / 2)
    benefits = "\n".join([
        benefit_on_bg(bx, ben_y0, bw, ico_flame, "Ho famonjena fanahin'olona"),
        benefit_on_bg(bx, ben_y0 + pill_h + pill_gap, bw, ico_star, "Ho fanasitranana ny aretina"),
        benefit_on_bg(bx, ben_y0 + 2 * (pill_h + pill_gap), bw, ico_leaf, "Ho fiainana mandrakizay ho anao"),
    ])

    day_labels = []
    for i, (name, time_s) in enumerate(zip(day_names, day_times)):
        xi = x0 + i * (item_w + gap)
        cx = xi + item_w / 2
        day_labels.append(T(cx, 418, name, size=20, fill=GOLD, weight="800", tracking="1.5", anchor="middle"))
        day_labels.append(T(cx, 446, time_s, size=18, fill=MUTED, weight="600", family="Open Sans", anchor="middle"))

    invite_w = min(1720, left_w - 30)
    invite_x = left_cx - invite_w / 2
    invite_y = 228
    invite_h = 130
    div_x = invite_x + invite_w * 0.52
    right_cx = (div_x + invite_x + invite_w) / 2

    cta_cx = pastor_x / 2
    cta_y = foot_y + foot_h / 2 + 8

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
  <title>Fitoriana Filazantsara Lehibe — Premium</title>
  <desc>Contenu gauche centré, timeline premium, pasteur compact</desc>

  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{IVORY}"/>
      <stop offset="65%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FFF6EC"/>
    </linearGradient>
    <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="12%" stop-color="#FFFFFF" stop-opacity="0.97"/>
      <stop offset="28%" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.68"/>
      <stop offset="62%" stop-color="#FFF9F2" stop-opacity="0.42"/>
      <stop offset="78%" stop-color="#FFF6EC" stop-opacity="0.2"/>
      <stop offset="90%" stop-color="#FFF5E8" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="lehibeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GOLD}"/>
      <stop offset="88%" stop-color="{GOLD}"/>
      <stop offset="100%" stop-color="#B87518"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#pageBg)"/>

  <image x="{PHOTO_X}" y="0" width="{PHOTO_W}" height="{H}"
         preserveAspectRatio="xMidYMid slice" xlink:href="{photo}" opacity="0.88"/>
  <rect x="{PHOTO_X - 280}" y="0" width="{FADE_W}" height="{H}" fill="url(#fadeL)"/>
  <rect x="{PHOTO_X - 160}" y="0" width="360" height="{H}" fill="url(#fadeL)" opacity="0.65"/>
  <rect x="{PHOTO_X - 60}" y="0" width="200" height="{H}" fill="url(#fadeL)" opacity="0.4"/>

  {benefits}

  <rect x="0" y="0" width="{W}" height="46" fill="{NAVY}"/>
  {T(W/2, 31, "FIANGONANA JESOSY MPAMONJY  ·  MORAFENO AMBOSITRA",
     size=19, fill=WHITE, weight="700", tracking="5", anchor="middle")}

  <!-- ===== LEFT CONTENT — centered as a group ===== -->
  {logo(left_cx - 680, 118, 2.1)}
  <text x="{left_cx + 40}" y="118" text-anchor="middle"
        font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="56" font-weight="800" letter-spacing="1.1">
    <tspan fill="{NAVY}">FITORIANA FILAZANTSARA</tspan>
    <tspan dx="28" fill="url(#lehibeGrad)">LEHIBE</tspan>
  </text>

  <text x="{left_cx}" y="168" text-anchor="middle"
        font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="22" font-weight="400" font-style="italic" fill="{INK}">
    “ Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, ka mitoria ny filazantsara amin'ny olombelona rehetra. ”
  </text>
  {ico_book(left_cx - 78, 196, 1.3)}
  <text x="{left_cx + 8}" y="202" text-anchor="middle"
        font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="19" font-weight="800" fill="{GOLD}">Marka 16:15</text>
  <rect x="{left_cx - 65}" y="214" width="130" height="4" rx="2" fill="{GOLD}"/>

  <!-- Invite two-column block centered -->
  <rect x="{invite_x}" y="{invite_y}" width="{invite_w}" height="{invite_h}" rx="18"
        fill="#F7F9FC" stroke="{LINE}" stroke-width="1.4"/>
  {people(invite_x + 58, invite_y + 65, 1.85)}
  <text x="{invite_x + 125}" y="{invite_y + 38}" font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="19" font-weight="600" fill="{MUTED}">Ny Mpitandrina sy ny fiangonana</text>
  <text x="{invite_x + 125}" y="{invite_y + 70}" font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="22" font-weight="800" fill="{NAVY}">JESOSY MPAMONJY MORAFENO AMBOSITRA</text>
  <text x="{invite_x + 125}" y="{invite_y + 102}" font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="19" font-weight="700" fill="{GOLD}">dia faly manasa antsika rehetra</text>
  <line x1="{div_x}" y1="{invite_y + 16}" x2="{div_x}" y2="{invite_y + invite_h - 16}"
        stroke="{LINE}" stroke-width="1.6"/>
  <text x="{right_cx}" y="{invite_y + 38}" text-anchor="middle"
        font-family="Open Sans, DejaVu Sans, sans-serif"
        font-size="17" font-weight="600" fill="{MUTED}">hanatrika ny Fitoriana Filazantsara Lehibe, iza atao ny</text>
  <rect x="{right_cx - 230}" y="{invite_y + 52}" width="280" height="56" rx="14" fill="{GOLD}"/>
  <text x="{right_cx - 90}" y="{invite_y + 88}" text-anchor="middle"
        font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="28" font-weight="800" fill="{NAVY}">6  ·  7  ·  8  ·  9</text>
  <text x="{right_cx + 70}" y="{invite_y + 74}" font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="20" font-weight="800" fill="{NAVY}">AOGOSITRA</text>
  <text x="{right_cx + 70}" y="{invite_y + 102}" font-family="Montserrat, DejaVu Sans, sans-serif"
        font-size="24" font-weight="800" fill="{NAVY}">2026</text>

  <!-- Schedule header — centered, one line -->
  <line x1="{left_x0}" y1="372" x2="{content_right}" y2="372" stroke="{LINE}" stroke-width="1.8"/>
  {T(left_cx, 402, "FANDAHARAM-POTOANA", size=22, fill=GOLD, weight="800", tracking="3", anchor="middle")}

  {"".join(day_labels)}
  {timeline}

  <rect x="0" y="{foot_y}" width="{W}" height="{foot_h}" fill="{NAVY}"/>
  <rect x="0" y="{foot_y}" width="{W}" height="3" fill="{GOLD}"/>

  {burst(cta_cx - 700, cta_y, False, 1.2)}
  <text x="{cta_cx}" y="{cta_y + 10}" text-anchor="middle"
        font-family="Great Vibes, Dancing Script, DejaVu Sans, sans-serif"
        font-size="42" font-weight="400">
    <tspan fill="{WHITE}">Anasana antsika rehetra hanatrika izany fotoana lehibe izany, </tspan>
    <tspan fill="{GOLD}">tongava handray ny anjaranao!</tspan>
  </text>
  {burst(cta_cx + 700, cta_y, True, 1.2)}

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
  <path d="M{pastor_x + pastor_w - 36} {pastor_y + 16}
           l2.8 7 7.5 1 -5.4 4.6 1.6 7.5 -6.5 -3.5 -6.5 3.5 1.6 -7.5 -5.4 -4.6 7.5 -1 z"
        fill="{WHITE}" opacity="0.22"/>

  {pastor_gold(pastor_x + 58, pastor_y + 72, 0.92)}
  {T(pastor_x + 98, pastor_y + 42, "Ny Mpitandrina:", size=13, fill=GOLD, weight="600")}
  {T(pastor_x + 98, pastor_y + 70, "RANDRIANARIZANANY", size=20, fill=WHITE, weight="800")}
  {T(pastor_x + 98, pastor_y + 94, "Lovasoa Fenomanana", size=14, fill=WHITE, weight="500", family="Open Sans")}
  {ico_phone(pastor_x + 112, pastor_y + 120, s=1.05)}
  {T(pastor_x + 130, pastor_y + 125, "Tel : 038 92 546 27  /  033 20 968 28", size=13.5, fill=WHITE, weight="600")}
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
    """Convert text to paths while preserving embedded <image> icons."""
    env = dict(**subprocess.os.environ)
    env["FONTCONFIG_FILE"] = "/tmp/fc/fonts.conf"
    actions = f"select-by-element:text;object-to-path;export-filename:{dest};export-type:svg;export-do"
    r = subprocess.run(["inkscape", str(src), f"--actions={actions}"],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0 or not dest.exists():
        shutil.copy(src, dest)
        print(f"OK outlined {dest.name} (fallback copy)")
        return

    # Inkscape outline export can drop <image>; reinject from source
    src_txt = src.read_text(encoding="utf-8")
    dest_txt = dest.read_text(encoding="utf-8")
    import re
    images = re.findall(r"<image\b[^>]*/>", src_txt)
    if images and dest_txt.count("<image") < len(images):
        # Insert images just before closing </svg>
        inject = "\n".join(images) + "\n"
        if "</svg>" in dest_txt:
            dest_txt = dest_txt.replace("</svg>", inject + "</svg>", 1)
            dest.write_text(dest_txt, encoding="utf-8")
            print(f"OK outlined {dest.name} (+{len(images)} images reinjected)")
        else:
            print(f"OK outlined {dest.name} (no </svg> to inject)")
    else:
        print(f"OK outlined {dest.name} (images={dest_txt.count('<image')})")


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
