#!/usr/bin/env python3
"""Build print-ready vector banner 3.00 m × 0.70 m (SVG + PDF + PNG)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path("/workspace")
OUT = ROOT / "banner"
ARTIFACTS = Path("/opt/cursor/artifacts")
PREVIEWS = ARTIFACTS / "screenshots"

NAVY = "#0B2A5B"
NAVY_DARK = "#071E42"
NAVY_MID = "#123A6F"
GOLD = "#E08A1E"
GOLD_DARK = "#C47312"
ORANGE = "#F0A020"
WHITE = "#FFFFFF"
GRAY = "#3D4A5C"
MUTED = "#6B7788"
LIGHT = "#E6EBF3"
GREEN = "#2F9E44"
BLUE = "#1E6BB8"

W, H = 3000, 700  # mm


def esc(t: str) -> str:
    return (
        t.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def T(
    x,
    y,
    content,
    *,
    size=20,
    fill=NAVY,
    family="Montserrat",
    weight="700",
    style="normal",
    anchor="start",
    tracking=None,
):
    a = [
        f'x="{x}"',
        f'y="{y}"',
        f'fill="{fill}"',
        f'font-family="{family}, DejaVu Sans, sans-serif"',
        f'font-size="{size}"',
        f'font-weight="{weight}"',
        f'font-style="{style}"',
        f'text-anchor="{anchor}"',
    ]
    if tracking is not None:
        a.append(f'letter-spacing="{tracking}"')
    return f"<text {' '.join(a)}>{esc(content)}</text>"


def wrap(s: str, max_chars: int) -> list[str]:
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [s]


def logo(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M-36 20 C-22 11 -8 11 0 15 C8 11 22 11 36 20 L36 28 C22 19 8 19 0 23 C-8 19 -22 19 -36 28 Z" fill="{NAVY}"/>
      <path d="M-31 20 C-18 13 -8 13 0 16 C8 13 18 13 31 20" fill="none" stroke="{GOLD}" stroke-width="2.2"/>
      <path d="M0 -34 L28 -12 V14 H-28 V-12 Z" fill="{NAVY}"/>
      <path d="M-32 -10 L0 -36 L32 -10" fill="none" stroke="{GOLD}" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>
      <rect x="-6.5" y="-1" width="13" height="15" rx="1.5" fill="{GOLD}"/>
      <circle cx="-12" cy="-13" r="4.2" fill="{GOLD}"/>
      <circle cx="0" cy="-15" r="5" fill="{ORANGE}"/>
      <circle cx="12" cy="-13" r="4.2" fill="{GOLD}"/>
      <path d="M-17.5 -5.5 C-17.5 -9.5 -15 -12.5 -12 -12.5 C-9 -12.5 -6.5 -9.5 -6.5 -5.5 Z" fill="{GOLD}"/>
      <path d="M-6.5 -4 C-6.5 -10.5 -3.5 -15.5 0 -15.5 C3.5 -15.5 6.5 -10.5 6.5 -4 Z" fill="{ORANGE}"/>
      <path d="M6.5 -5.5 C6.5 -9.5 9 -12.5 12 -12.5 C15 -12.5 17.5 -9.5 17.5 -5.5 Z" fill="{GOLD}"/>
    </g>"""


def people(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="30" fill="{NAVY}"/>
      <circle cx="-11" cy="-5" r="6.5" fill="{GOLD}"/>
      <circle cy="-8" r="7.5" fill="{ORANGE}"/>
      <circle cx="11" cy="-5" r="6.5" fill="{GOLD}"/>
      <path d="M-20 16 C-20 7 -15 2 -11 2 C-7 2 -4 6 -3.5 11" fill="{GOLD}"/>
      <path d="M-9 18 C-9 6 -4 0 0 0 C4 0 9 6 9 18 Z" fill="{ORANGE}"/>
      <path d="M3.5 11 C4 6 7 2 11 2 C15 2 20 7 20 16" fill="{GOLD}"/>
    </g>"""


def flame(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="15" fill="{GOLD}"/>
      <path d="M0 9 C-7 2 -6 -5 -2 -10 C-0.5 -4 2.5 -6 3.5 -11 C9 -4 8 4 0 9 Z" fill="{WHITE}"/>
    </g>"""


def star(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="15" fill="{BLUE}"/>
      <path d="M0 -8.5 L2.1 -2.3 L8.5 -2.3 L3.3 1.4 L5.2 7.5 L0 3.8 L-5.2 7.5 L-3.3 1.4 L-8.5 -2.3 L-2.1 -2.3 Z" fill="{WHITE}"/>
    </g>"""


def leaf(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="15" fill="{GREEN}"/>
      <path d="M0 8.5 C-7.5 1.5 -7.5 -6 0 -9.5 C7.5 -6 7.5 1.5 0 8.5 Z" fill="{WHITE}"/>
      <path d="M0 7.5 V-8" stroke="{GREEN}" stroke-width="1.4"/>
    </g>"""


def calendar(cx, cy, day, s=1.0):
    return f"""
    <g transform="translate({cx - 15*s},{cy - 16*s}) scale({s})">
      <rect y="5" width="30" height="27" rx="4" fill="{GOLD}"/>
      <rect y="5" width="30" height="9" rx="3" fill="{NAVY}"/>
      <rect x="2.5" y="16" width="25" height="13.5" rx="2" fill="{WHITE}"/>
      <circle cx="8" cy="3" r="2.2" fill="{NAVY}"/>
      <circle cx="22" cy="3" r="2.2" fill="{NAVY}"/>
      {T(15, 27, str(day), size=13, fill=NAVY, weight="800", anchor="middle")}
    </g>"""


def clock(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="10.5" fill="none" stroke="{GOLD}" stroke-width="2.4"/>
      <circle r="1.7" fill="{GOLD}"/>
      <path d="M0 -5.5 V0 H4.8" fill="none" stroke="{NAVY}" stroke-width="2" stroke-linecap="round"/>
    </g>"""


def pin(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M0 -10 C-6.8 -10 -11 -4.2 -11 0.8 C-11 7.5 0 15 0 15 C0 15 11 7.5 11 0.8 C11 -4.2 6.8 -10 0 -10 Z" fill="{GOLD}"/>
      <circle cy="-0.5" r="3.3" fill="{WHITE}"/>
    </g>"""


def book(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M-11 7 C-5 3.5 0 3.5 0 3.5 C0 3.5 5 3.5 11 7 V-7 C5 -10.5 0 -10.5 0 -10.5 C0 -10.5 -5 -10.5 -11 -7 Z" fill="{GOLD}"/>
      <path d="M0 -10.5 V3.5" stroke="{WHITE}" stroke-width="1.2"/>
    </g>"""


def pastor(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="20" fill="{WHITE}" opacity="0.12"/>
      <circle cy="-5.5" r="6.5" fill="{WHITE}"/>
      <path d="M-13 15 C-13 5.5 -7.5 1.5 0 1.5 C7.5 1.5 13 5.5 13 15 Z" fill="{WHITE}"/>
    </g>"""


def phone(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <rect x="-6.5" y="-10.5" width="13" height="21" rx="2.8" fill="none" stroke="{GOLD}" stroke-width="2"/>
      <circle cy="7.2" r="1.4" fill="{GOLD}"/>
      <line x1="-2.8" y1="-7.5" x2="2.8" y2="-7.5" stroke="{GOLD}" stroke-width="1.4"/>
    </g>"""


def wheat(cx, cy, flip=False):
    sx = -1 if flip else 1
    return f"""
    <g transform="translate({cx},{cy}) scale({sx},1)" fill="{GOLD}">
      <path d="M0 2 C18 -14 38 -18 56 -12 C38 -6 20 0 0 2 Z" opacity="0.95"/>
      <path d="M6 0 C24 -20 46 -28 68 -22 C48 -14 28 -4 6 0 Z" opacity="0.72"/>
      <path d="M12 6 C30 -4 50 -4 68 4 C50 8 32 12 12 6 Z" opacity="0.88"/>
      <ellipse cx="56" cy="-12" rx="4.5" ry="2.6" transform="rotate(-22 56 -12)"/>
      <ellipse cx="68" cy="-22" rx="4.5" ry="2.6" transform="rotate(-32 68 -22)"/>
      <ellipse cx="68" cy="4" rx="4.5" ry="2.6" transform="rotate(-8 68 4)"/>
    </g>"""


def crowd(x, y, w, h):
    return f"""
    <defs>
      <linearGradient id="sunset" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#FFC45A"/>
        <stop offset="40%" stop-color="#FF8F1F"/>
        <stop offset="75%" stop-color="#D94E0F"/>
        <stop offset="100%" stop-color="#7A2408"/>
      </linearGradient>
      <clipPath id="crowdClip"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath>
    </defs>
    <g clip-path="url(#crowdClip)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sunset)"/>
      <circle cx="{x + w*0.78}" cy="{y + h*0.36}" r="{h*0.2}" fill="#FFE49A" opacity="0.95"/>
      <ellipse cx="{x + w*0.28}" cy="{y + h*0.2}" rx="{w*0.16}" ry="{h*0.07}" fill="#FFF1D0" opacity="0.45"/>
      <ellipse cx="{x + w*0.55}" cy="{y + h*0.16}" rx="{w*0.12}" ry="{h*0.05}" fill="#FFF1D0" opacity="0.35"/>
      <path fill="#140C18" d="
        M{x} {y+h} L{x} {y+h*0.78}
        C{x+w*0.04} {y+h*0.58} {x+w*0.07} {y+h*0.52} {x+w*0.11} {y+h*0.58}
        C{x+w*0.13} {y+h*0.44} {x+w*0.17} {y+h*0.42} {x+w*0.19} {y+h*0.54}
        C{x+w*0.22} {y+h*0.38} {x+w*0.27} {y+h*0.34} {x+w*0.29} {y+h*0.52}
        C{x+w*0.33} {y+h*0.3} {x+w*0.39} {y+h*0.28} {x+w*0.41} {y+h*0.5}
        C{x+w*0.45} {y+h*0.32} {x+w*0.5} {y+h*0.3} {x+w*0.52} {y+h*0.52}
        C{x+w*0.56} {y+h*0.34} {x+w*0.61} {y+h*0.32} {x+w*0.63} {y+h*0.54}
        C{x+w*0.67} {y+h*0.38} {x+w*0.72} {y+h*0.36} {x+w*0.74} {y+h*0.56}
        C{x+w*0.78} {y+h*0.42} {x+w*0.83} {y+h*0.4} {x+w*0.86} {y+h*0.58}
        C{x+w*0.91} {y+h*0.48} {x+w*0.96} {y+h*0.54} {x+w} {y+h*0.66}
        L{x+w} {y+h} Z"/>
      <path d="M{x+w*0.2} {y+h*0.54} C{x+w*0.19} {y+h*0.34} {x+w*0.18} {y+h*0.24} {x+w*0.19} {y+h*0.16}"
            fill="none" stroke="#140C18" stroke-width="3.2" stroke-linecap="round"/>
      <path d="M{x+w*0.4} {y+h*0.5} C{x+w*0.39} {y+h*0.3} {x+w*0.41} {y+h*0.18} {x+w*0.42} {y+h*0.12}"
            fill="none" stroke="#140C18" stroke-width="3.2" stroke-linecap="round"/>
      <path d="M{x+w*0.6} {y+h*0.54} C{x+w*0.61} {y+h*0.32} {x+w*0.59} {y+h*0.2} {x+w*0.6} {y+h*0.13}"
            fill="none" stroke="#140C18" stroke-width="3.2" stroke-linecap="round"/>
      <path d="M{x+w*0.78} {y+h*0.56} C{x+w*0.79} {y+h*0.36} {x+w*0.81} {y+h*0.24} {x+w*0.8} {y+h*0.17}"
            fill="none" stroke="#140C18" stroke-width="3.2" stroke-linecap="round"/>
    </g>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{GOLD}" stroke-width="2.5"/>"""


def day_card(x, y, w, h, name, num, time_s, place_lines):
    hh = 32
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{WHITE}" stroke="{LIGHT}" stroke-width="2"/>
      <path d="M{x} {y+10} Q{x} {y} {x+10} {y} H{x+w-10} Q{x+w} {y} {x+w} {y+10} V{y+hh} H{x} Z" fill="{NAVY}"/>
      <rect x="{x}" y="{y+hh-7}" width="{w}" height="8" fill="{GOLD}"/>
      {T(x + w/2, y + 21, name, size=14, fill=WHITE, weight="800", anchor="middle", tracking="1.8")}
      {calendar(x + 26, y + hh + 24, num, 0.95)}
      {T(x + 48, y + hh + 22, f"{num} Aogositra 2026", size=14, fill=NAVY, weight="700")}
      {clock(x + 20, y + hh + 48, 0.95)}
      {T(x + 38, y + hh + 52, time_s, size=12, fill=MUTED, weight="600", family="Open Sans")}
      {pin(x + 20, y + hh + 76, 0.9)}
      {T(x + 38, y + hh + 70, place_lines[0], size=12, fill=GRAY, weight="700")}
      {T(x + 38, y + hh + 88, place_lines[1], size=12, fill=MUTED, weight="600", family="Open Sans")}
    </g>"""


def build_svg() -> str:
    days = [
        ("ALAKAMISY", "6", "@ 15:00  ·  3 ora tolakandro",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
        ("ZOMA", "7", "@ 15:00  ·  3 ora tolakandro",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
        ("SABOTSY", "8", "@ 15:00  ·  3 ora tolakandro",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
        ("ALAHADY", "9", "@ 09:00  ·  9 ora maraina",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
    ]

    card_w, gap = 690, 20
    total = 4 * card_w + 3 * gap
    x0 = (W - total) / 2
    cards = "\n".join(
        day_card(x0 + i * (card_w + gap), 372, card_w, 148, *d)
        for i, d in enumerate(days)
    )

    q_lines = wrap(
        "Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, "
        "ka mitoria ny filazantsara amin'ny olombelona rehetra.",
        95,
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm"
     viewBox="0 0 {W} {H}" version="1.1">
  <title>Fitoriana Filazantsara Lehibe — 6-9 Aogositra 2026 — Morafeno Ambositra</title>
  <desc>Banderole vectorielle impression 3,00 m × 0,70 m — Fiangonana Jesosy Mpamonjy Morafeno Ambositra</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#F5F8FC"/>
      <stop offset="100%" stop-color="#E9EEF6"/>
    </linearGradient>
    </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <rect width="{W}" height="40" fill="{NAVY_DARK}"/>
  {T(W/2, 27, "FIANGONANA JESOSY MPAMONJY MORAFENO AMBOSITRA",
     size=18, fill=WHITE, weight="700", anchor="middle", tracking="5")}

  {logo(95, 118, 1.4)}
  {T(175, 98, "FITORIANA FILAZANTSARA", size=52, fill=NAVY, weight="800", tracking="1")}
  {T(175, 155, "LEHIBE", size=58, fill=GOLD, weight="800", tracking="8")}
  {crowd(2240, 52, 700, 125)}

  <g>
    {T(90, 205, "“", size=58, fill=GOLD, family="Great Vibes", weight="400")}
    {T(140, 200, q_lines[0], size=17, fill=NAVY, family="Open Sans", weight="400", style="italic")}
    {T(140, 224, q_lines[1] if len(q_lines) > 1 else "", size=17, fill=NAVY, family="Open Sans", weight="400", style="italic")}
    {T(1980, 220, "”", size=58, fill=GOLD, family="Great Vibes", weight="400")}
    {book(2055, 208, 1.35)}
    {T(2080, 214, "Marka 16:15", size=16, fill=GOLD_DARK, weight="700")}
  </g>

  <line x1="80" y1="245" x2="2920" y2="245" stroke="{LIGHT}" stroke-width="2"/>

  {people(115, 300, 1.05)}
  {T(165, 282, "Ny Mpitandrina sy ny fiangonana", size=15, fill=GRAY, weight="600", family="Open Sans")}
  {T(165, 304, "JESOSY MPAMONJY MORAFENO AMBOSITRA", size=16, fill=NAVY, weight="800")}
  {T(165, 326, "dia faly manasa antsika rehetra", size=15, fill=GRAY, weight="600", family="Open Sans")}

  <line x1="720" y1="262" x2="720" y2="335" stroke="{LIGHT}" stroke-width="2"/>

  {T(1180, 272, "Hanatrika ny Fitoriana Filazantsara Lehibe, izay atao ny",
     size=14, fill=MUTED, weight="600", anchor="middle", family="Open Sans")}
  <rect x="860" y="285" width="360" height="50" rx="12" fill="{GOLD}"/>
  {T(1040, 319, "6  ·  7  ·  8  ·  9", size=30, fill=NAVY, weight="800", anchor="middle")}
  {T(1250, 319, "AOGOSITRA 2026", size=24, fill=NAVY, weight="800")}
  <rect x="970" y="342" width="260" height="22" rx="4" fill="{NAVY}"/>
  {T(1100, 358, "FANDAHARAM-POTOANA", size=12, fill=WHITE, weight="700", anchor="middle", tracking="1.6")}

  <line x1="1620" y1="262" x2="1620" y2="360" stroke="{LIGHT}" stroke-width="2"/>

  {flame(1685, 278, 1.05)}
  {T(1715, 284, "Ho famonjena fanahin'olona", size=17, fill=NAVY, weight="700")}
  {star(1685, 316, 1.05)}
  {T(1715, 322, "Ho fanasitranana ny aretina", size=17, fill=NAVY, weight="700")}
  {leaf(1685, 354, 1.05)}
  {T(1715, 360, "Ho fiainana mandrakizay ho anao", size=17, fill=NAVY, weight="700")}

  {cards}

  <rect x="0" y="530" width="{W}" height="170" fill="{NAVY_DARK}"/>
  <rect x="0" y="530" width="{W}" height="7" fill="{GOLD}"/>

  {wheat(160, 605, False)}
  {T(1000, 595, "Anasana antsika rehetra hanatrika izany fotoana lehibe izany,",
     size=32, fill=GOLD, family="Dancing Script", weight="700", anchor="middle")}
  {T(1000, 645, "tongava handray ny anjaranao!",
     size=36, fill=GOLD, family="Dancing Script", weight="700", anchor="middle")}
  {wheat(1840, 605, True)}

  <rect x="1980" y="555" width="940" height="120" rx="14" fill="{NAVY_MID}"/>
  <rect x="1980" y="555" width="8" height="120" fill="{GOLD}"/>
  {pastor(2050, 615, 1.4)}
  {T(2100, 590, "Ny Mpitandrina", size=14, fill=GOLD, weight="600")}
  {T(2100, 618, "RANDRIANARIZANANY Lovasoa Fenomanana", size=18, fill=WHITE, weight="700")}
  {phone(2110, 652, 1.15)}
  {T(2135, 658, "038 92 546 27   /   033 20 968 28", size=18, fill=WHITE, weight="700")}
</svg>
"""


def inkscape_export(svg: Path, out: Path, *, export_type: str, dpi: int | None = None, width: int | None = None):
    cmd = [
        "inkscape",
        str(svg),
        f"--export-type={export_type}",
        f"--export-filename={out}",
    ]
    if dpi:
        cmd.append(f"--export-dpi={dpi}")
    if width:
        cmd.append(f"--export-width={width}")
    env = dict(**subprocess.os.environ)
    env["FONTCONFIG_FILE"] = "/tmp/fc/fonts.conf"
    Path("/tmp/fc").mkdir(exist_ok=True)
    Path("/tmp/fc/fonts.conf").write_text(
        """<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir>/workspace/fonts</dir>
  <dir>/home/ubuntu/.fonts</dir>
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
</fontconfig>
"""
    )
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        print("STDERR:", r.stderr[-2000:])
        raise RuntimeError(f"inkscape failed for {out}")
    print(f"OK {out} ({out.stat().st_size/1e6:.2f} MB)")


def text_to_paths(src: Path, dest: Path):
    """Convert text to outlines for print-shop safety."""
    env = dict(**subprocess.os.environ)
    env["FONTCONFIG_FILE"] = "/tmp/fc/fonts.conf"
    # Inkscape actions: select all text, object to path
    actions = (
        "select-by-element:text;"
        "object-to-path;"
        f"export-filename:{dest};"
        "export-type:svg;"
        "export-do"
    )
    r = subprocess.run(
        ["inkscape", str(src), f"--actions={actions}"],
        capture_output=True,
        text=True,
        env=env,
    )
    if r.returncode != 0 or not dest.exists():
        # fallback: copy + note
        print("text-to-path warning:", r.stderr[-1500:])
        shutil.copy(src, dest)
    else:
        print(f"OK outlined {dest} ({dest.stat().st_size/1e6:.2f} MB)")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    svg_path = OUT / "banderole-3m-x-70cm.svg"
    svg_path.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote editable SVG {svg_path}")

    # Outlined SVG (no font dependency)
    outlined = OUT / "banderole-3m-x-70cm-outlined.svg"
    text_to_paths(svg_path, outlined)

    # PDF vector (prefer outlined — no font dependency at print shop)
    pdf = OUT / "banderole-3m-x-70cm.pdf"
    inkscape_export(outlined if outlined.exists() else svg_path, pdf, export_type="pdf")

    # Editable PDF (text still selectable) as secondary
    pdf_edit = OUT / "banderole-3m-x-70cm-editable.pdf"
    inkscape_export(svg_path, pdf_edit, export_type="pdf")

    # Preview PNG
    preview = PREVIEWS / "banderole-preview.png"
    inkscape_export(svg_path, preview, export_type="png", width=3000)

    # HD raster at 150 DPI (standard large-format)
    hd = OUT / "banderole-3m-x-70cm-150dpi.png"
    inkscape_export(svg_path, hd, export_type="png", dpi=150)

    proof = OUT / "banderole-proof.png"
    inkscape_export(svg_path, proof, export_type="png", width=9000)

    for src in [svg_path, outlined, pdf, preview]:
        if src.exists():
            dest = ARTIFACTS / src.name
            shutil.copy(src, dest)
            print("artifact", dest)


if __name__ == "__main__":
    main()
