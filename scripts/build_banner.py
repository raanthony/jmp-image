#!/usr/bin/env python3
"""
Faithful vector recreation of the Fitoriana Filazantsara flyer
for print as a 3.00 m × 0.70 m banner.
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

# Palette matched to original flyer
NAVY = "#0A2A5C"
NAVY_DARK = "#071E42"
NAVY_MID = "#123A6F"
GOLD = "#E0891C"
GOLD_SOFT = "#F0A94A"
ORANGE = "#F09420"
WHITE = "#FFFFFF"
OFF = "#FBFCFE"
GRAY = "#3A4658"
MUTED = "#6A7688"
LINE = "#D8DEE8"
GREEN = "#2F9E44"
BLUE = "#1E6BB8"

W, H = 3000, 700  # mm units


def esc(t: str) -> str:
    return (
        t.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def T(
    x, y, content, *, size=20, fill=NAVY, family="Montserrat",
    weight="700", style="normal", anchor="start", tracking=None,
):
    a = [
        f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
        f'font-family="{family}, DejaVu Sans, sans-serif"',
        f'font-size="{size}"', f'font-weight="{weight}"',
        f'font-style="{style}"', f'text-anchor="{anchor}"',
    ]
    if tracking is not None:
        a.append(f'letter-spacing="{tracking}"')
    return f"<text {' '.join(a)}>{esc(content)}</text>"


def wrap(s: str, n: int) -> list[str]:
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if len(t) <= n:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [s]


def img_href(path: Path) -> str:
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode()
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{b64}"


# ---------------- icons (faithful to flyer) ----------------

def logo(cx, cy, s=1.0):
    """Church house with 3 people on open book — navy + gold."""
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <!-- open book base -->
      <path d="M-38 22 C-24 12 -10 11 0 16 C10 11 24 12 38 22
               L38 30 C24 20 10 19 0 24 C-10 19 -24 20 -38 30 Z" fill="{NAVY}"/>
      <path d="M-33 22 C-20 14 -8 14 0 17.5 C8 14 20 14 33 22"
            fill="none" stroke="{GOLD}" stroke-width="2.4"/>
      <!-- house body -->
      <path d="M-26 -10 L-26 14 L26 14 L26 -10 L0 -34 Z" fill="{NAVY}"/>
      <!-- gold roof outline -->
      <path d="M-32 -8 L0 -38 L32 -8" fill="none" stroke="{GOLD}"
            stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
      <!-- door -->
      <rect x="-7" y="0" width="14" height="14" rx="1.5" fill="{GOLD}"/>
      <!-- three people -->
      <circle cx="-13" cy="-12" r="4.4" fill="{GOLD}"/>
      <circle cx="0" cy="-15" r="5.2" fill="{ORANGE}"/>
      <circle cx="13" cy="-12" r="4.4" fill="{GOLD}"/>
      <path d="M-19 -4.5 C-19 -9 -16.5 -12.5 -13 -12.5 C-9.5 -12.5 -7 -9 -7 -4.5 Z" fill="{GOLD}"/>
      <path d="M-7 -3 C-7 -10.5 -3.8 -15.5 0 -15.5 C3.8 -15.5 7 -10.5 7 -3 Z" fill="{ORANGE}"/>
      <path d="M7 -4.5 C7 -9 9.5 -12.5 13 -12.5 C16.5 -12.5 19 -9 19 -4.5 Z" fill="{GOLD}"/>
    </g>"""


def people_circle(cx, cy, s=1.0):
    """Circular embrace icon."""
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="32" fill="{NAVY}"/>
      <circle r="32" fill="none" stroke="{GOLD}" stroke-width="2.5"/>
      <circle cx="-12" cy="-6" r="7" fill="{GOLD}"/>
      <circle cy="-9" r="8" fill="{ORANGE}"/>
      <circle cx="12" cy="-6" r="7" fill="{GOLD}"/>
      <path d="M-22 18 C-22 8 -17 2 -12 2 C-7 2 -4 7 -3 12" fill="{GOLD}"/>
      <path d="M-10 20 C-10 6 -5 -1 0 -1 C5 -1 10 6 10 20 Z" fill="{ORANGE}"/>
      <path d="M3 12 C4 7 7 2 12 2 C17 2 22 8 22 18" fill="{GOLD}"/>
    </g>"""


def flame(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="16" fill="{GOLD}"/>
      <path d="M0 10 C-8 2 -7 -5 -2.5 -11 C-1 -4 3 -7 4 -12 C10 -4 9 4 0 10 Z" fill="{WHITE}"/>
    </g>"""


def star_ico(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="16" fill="{BLUE}"/>
      <path d="M0 -9.5 L2.4 -2.6 L9.5 -2.6 L3.7 1.6 L5.8 8.5 L0 4.2 L-5.8 8.5 L-3.7 1.6 L-9.5 -2.6 L-2.4 -2.6 Z" fill="{WHITE}"/>
    </g>"""


def leaf_ico(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="16" fill="{GREEN}"/>
      <path d="M0 9.5 C-8.5 1.5 -8.5 -7 0 -11 C8.5 -7 8.5 1.5 0 9.5 Z" fill="{WHITE}"/>
      <path d="M0 8 V-9.5" stroke="{GREEN}" stroke-width="1.5"/>
    </g>"""


def calendar(cx, cy, day, s=1.0):
    return f"""
    <g transform="translate({cx-16*s},{cy-17*s}) scale({s})">
      <rect y="5" width="32" height="28" rx="4" fill="{GOLD}"/>
      <rect y="5" width="32" height="9" rx="3" fill="{NAVY}"/>
      <rect x="2.5" y="16.5" width="27" height="14" rx="2" fill="{WHITE}"/>
      <circle cx="8" cy="3" r="2.3" fill="{NAVY}"/>
      <circle cx="24" cy="3" r="2.3" fill="{NAVY}"/>
      {T(16, 28, str(day), size=13, fill=NAVY, weight="800", anchor="middle")}
    </g>"""


def clock(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="11" fill="none" stroke="{GOLD}" stroke-width="2.5"/>
      <circle r="1.8" fill="{GOLD}"/>
      <path d="M0 -6 V0 H5" fill="none" stroke="{NAVY}" stroke-width="2.1" stroke-linecap="round"/>
    </g>"""


def pin(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M0 -11 C-7.2 -11 -11.5 -4.5 -11.5 0.7 C-11.5 8 0 16 0 16
               C0 16 11.5 8 11.5 0.7 C11.5 -4.5 7.2 -11 0 -11 Z" fill="{GOLD}"/>
      <circle cy="-0.3" r="3.5" fill="{WHITE}"/>
    </g>"""


def book(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <path d="M-12 8 C-5.5 3.5 0 3.5 0 3.5 C0 3.5 5.5 3.5 12 8
               V-8 C5.5 -12 0 -12 0 -12 C0 -12 -5.5 -12 -12 -8 Z" fill="{GOLD}"/>
      <path d="M0 -12 V3.5" stroke="{WHITE}" stroke-width="1.3"/>
    </g>"""


def pastor(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <circle r="22" fill="{WHITE}" opacity="0.14"/>
      <circle cy="-6" r="7.2" fill="{WHITE}"/>
      <path d="M-14 16 C-14 5.5 -8 1.2 0 1.2 C8 1.2 14 5.5 14 16 Z" fill="{WHITE}"/>
    </g>"""


def phone(cx, cy, s=1.0):
    return f"""
    <g transform="translate({cx},{cy}) scale({s})">
      <rect x="-7" y="-11.5" width="14" height="23" rx="3" fill="none" stroke="{GOLD}" stroke-width="2.1"/>
      <circle cy="8" r="1.5" fill="{GOLD}"/>
      <line x1="-3" y1="-8" x2="3" y2="-8" stroke="{GOLD}" stroke-width="1.5"/>
    </g>"""


def wheat(cx, cy, flip=False):
    sx = -1 if flip else 1
    return f"""
    <g transform="translate({cx},{cy}) scale({sx},1)" fill="{GOLD}">
      <path d="M0 2 C20 -16 42 -20 62 -14 C42 -7 22 0 0 2 Z" opacity="0.95"/>
      <path d="M7 0 C26 -22 50 -30 74 -24 C52 -15 30 -4 7 0 Z" opacity="0.7"/>
      <path d="M14 7 C34 -4 56 -4 76 5 C56 10 36 14 14 7 Z" opacity="0.88"/>
      <ellipse cx="62" cy="-14" rx="5" ry="2.8" transform="rotate(-24 62 -14)"/>
      <ellipse cx="74" cy="-24" rx="5" ry="2.8" transform="rotate(-34 74 -24)"/>
      <ellipse cx="76" cy="5" rx="5" ry="2.8" transform="rotate(-8 76 5)"/>
    </g>"""


def day_card(x, y, w, h, name, num, time_s, places):
    """Orange + navy header as on original flyer."""
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{WHITE}"
            stroke="{LINE}" stroke-width="2"/>
      <!-- navy header -->
      <path d="M{x} {y+11} Q{x} {y} {x+11} {y} H{x+w-11} Q{x+w} {y} {x+w} {y+11}
               V{y+30} H{x} Z" fill="{NAVY}"/>
      <!-- orange accent under header -->
      <rect x="{x}" y="{y+28}" width="{w}" height="9" fill="{GOLD}"/>
      {T(x + w/2, y + 21, f"{name}  ·  {num}", size=14, fill=WHITE, weight="800",
         anchor="middle", tracking="1.2")}
      {calendar(x + 28, y + 62, num, 1.0)}
      {T(x + 52, y + 58, f"{num} Aogositra 2026", size=14, fill=NAVY, weight="700")}
      {clock(x + 22, y + 90, 1.0)}
      {T(x + 40, y + 94, time_s, size=12.5, fill=MUTED, weight="600", family="Open Sans")}
      {pin(x + 22, y + 120, 0.95)}
      {T(x + 40, y + 114, places[0], size=12.5, fill=GRAY, weight="700")}
      {T(x + 40, y + 132, places[1], size=12, fill=MUTED, weight="600", family="Open Sans")}
    </g>"""


def build_svg() -> str:
    crowd = ASSETS / "crowd-sunset-wide.jpg"
    crowd_data = img_href(crowd)

    # Schedule — style of original (@ 3 ora tolakandro example)
    days = [
        ("ALAKAMISY", "6", "@ 15:00   3 ora tolakandro",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
        ("ZOMA", "7", "@ 15:00   3 ora tolakandro",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
        ("SABOTSY", "8", "@ 15:00   3 ora tolakandro",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
        ("ALAHADY", "9", "@ 09:00   9 ora maraina",
         ["Fiangonana Jesosy Mpamonjy", "Morafeno — Ambositra"]),
    ]

    card_w, gap = 700, 18
    total = 4 * card_w + 3 * gap
    x0 = (W - total) / 2
    cards = "\n".join(
        day_card(x0 + i * (card_w + gap), 365, card_w, 150, *d)
        for i, d in enumerate(days)
    )

    q = wrap(
        "Ary hoy Izy taminy: Mandehana any amin'izao tontolo izao ianareo, "
        "ka mitoria ny filazantsara amin'ny olombelona rehetra.",
        92,
    )

    # Crowd panel geometry
    cx, cy, cw, ch = 2180, 52, 760, 130

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
  <title>Fitoriana Filazantsara Lehibe — Morafeno Ambositra — 6-9 Aogositra 2026</title>
  <desc>Banderole vectorielle 3,00×0,70 m d'après le flyer original</desc>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#E8EEF6"/>
    </linearGradient>
    <clipPath id="crowdClip">
      <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14"/>
    </clipPath>
  </defs>

  <!-- BACKGROUND -->
  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <!-- ========== TOP BAR ========== -->
  <rect width="{W}" height="40" fill="{NAVY_DARK}"/>
  {T(W/2, 27, "FIANGONANA JESOSY MPAMONJY MORAFENO AMBOSITRA",
     size=18, fill=WHITE, weight="700", anchor="middle", tracking="5")}

  <!-- ========== HEADER ========== -->
  {logo(100, 120, 1.45)}
  {T(180, 100, "FITORIANA FILAZANTSARA", size=50, fill=NAVY, weight="800", tracking="0.5")}
  {T(180, 156, "LEHIBE", size=56, fill=GOLD, weight="800", tracking="7")}

  <!-- Top-right crowd / sunset photo (as on original) -->
  <g clip-path="url(#crowdClip)">
    <image x="{cx}" y="{cy}" width="{cw}" height="{ch}"
           preserveAspectRatio="xMidYMid slice"
           xlink:href="{crowd_data}"/>
  </g>
  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14"
        fill="none" stroke="{GOLD}" stroke-width="3"/>

  <!-- ========== QUOTE ========== -->
  <g>
    {T(95, 208, "“", size=62, fill=GOLD, family="Great Vibes", weight="400")}
    {T(145, 202, q[0], size=16.5, fill=NAVY, family="Open Sans", weight="400", style="italic")}
    {T(145, 226, q[1] if len(q)>1 else '', size=16.5, fill=NAVY, family="Open Sans", weight="400", style="italic")}
    {T(1920, 222, "”", size=62, fill=GOLD, family="Great Vibes", weight="400")}
    {book(2000, 210, 1.4)}
    {T(2028, 216, "Marka 16:15", size=16, fill=GOLD, weight="700")}
  </g>

  <line x1="70" y1="248" x2="2930" y2="248" stroke="{LINE}" stroke-width="2"/>

  <!-- ========== MID ROW ========== -->
  <!-- left invite -->
  {people_circle(118, 305, 1.0)}
  {T(170, 286, "Ny Mpitandrina sy ny fiangonana", size=14.5, fill=MUTED, weight="600", family="Open Sans")}
  {T(170, 308, "JESOSY MPAMONJY MORAFENO AMBOSITRA", size=15.5, fill=NAVY, weight="800")}
  {T(170, 330, "dia faly manasa antsika rehetra", size=14.5, fill=MUTED, weight="600", family="Open Sans")}

  <line x1="740" y1="268" x2="740" y2="345" stroke="{LINE}" stroke-width="2"/>

  <!-- center dates -->
  {T(1180, 275, "Hanatrika ny Fitoriana Filazantsara Lehibe, izay atao ny",
     size=13.5, fill=MUTED, weight="600", anchor="middle", family="Open Sans")}
  <rect x="860" y="288" width="360" height="52" rx="14" fill="{GOLD}"/>
  {T(1040, 323, "6  -  7  -  8  -  9", size=30, fill=NAVY, weight="800", anchor="middle")}
  {T(1255, 323, "AOGOSITRA 2026", size=24, fill=NAVY, weight="800")}
  <rect x="980" y="348" width="240" height="22" rx="4" fill="{NAVY}"/>
  {T(1100, 364, "FANDAHARAM-POTOANA", size=11.5, fill=WHITE, weight="700",
     anchor="middle", tracking="1.5")}

  <line x1="1600" y1="268" x2="1600" y2="365" stroke="{LINE}" stroke-width="2"/>

  <!-- benefits -->
  {flame(1670, 282, 1.05)}
  {T(1700, 288, "Ho famonjena fanahin'olona", size=16.5, fill=NAVY, weight="700")}
  {star_ico(1670, 320, 1.05)}
  {T(1700, 326, "Ho fanasitranana ny aretina", size=16.5, fill=NAVY, weight="700")}
  {leaf_ico(1670, 358, 1.05)}
  {T(1700, 364, "Ho fiainana mandrakizay ho anao", size=16.5, fill=NAVY, weight="700")}

  <!-- ========== SCHEDULE ========== -->
  {cards}

  <!-- ========== FOOTER ========== -->
  <rect x="0" y="528" width="{W}" height="172" fill="{NAVY_DARK}"/>
  <rect x="0" y="528" width="{W}" height="7" fill="{GOLD}"/>

  {wheat(150, 605, False)}
  {T(1020, 595, "Anasana antsika rehetra hanatrika izany fotoana lehibe izany,",
     size=30, fill=GOLD, family="Dancing Script", weight="700", anchor="middle")}
  {T(1020, 645, "tongava handray ny anjaranao!",
     size=34, fill=GOLD, family="Dancing Script", weight="700", anchor="middle")}
  {wheat(1890, 605, True)}

  <!-- contact block -->
  <rect x="2020" y="552" width="900" height="122" rx="14" fill="{NAVY_MID}"/>
  <rect x="2020" y="552" width="8" height="122" fill="{GOLD}"/>
  {pastor(2088, 613, 1.35)}
  {T(2135, 588, "Ny Mpitandrina:", size=14, fill=GOLD, weight="600")}
  {T(2135, 616, "RANDRIANARIZANANY Lovasoa Fenomanana", size=17.5, fill=WHITE, weight="700")}
  {phone(2145, 650, 1.1)}
  {T(2170, 656, "038 92 546 27  /  033 20 968 28", size=17.5, fill=WHITE, weight="700")}
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
</fontconfig>
"""
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
        print(r.stderr[-1500:])
        raise RuntimeError(f"inkscape failed: {out}")
    print(f"OK {out.name} ({out.stat().st_size/1e6:.2f} MB)")


def outline_text(src: Path, dest: Path):
    env = dict(**subprocess.os.environ)
    env["FONTCONFIG_FILE"] = "/tmp/fc/fonts.conf"
    actions = (
        "select-by-element:text;object-to-path;"
        f"export-filename:{dest};export-type:svg;export-do"
    )
    r = subprocess.run(
        ["inkscape", str(src), f"--actions={actions}"],
        capture_output=True, text=True, env=env,
    )
    if r.returncode != 0 or not dest.exists():
        print("outline warn:", r.stderr[-800:])
        shutil.copy(src, dest)
    else:
        print(f"OK outlined {dest.name} ({dest.stat().st_size/1e6:.2f} MB)")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)

    svg = OUT / "banderole-3m-x-70cm.svg"
    svg.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {svg} ({svg.stat().st_size/1e6:.2f} MB)")

    outlined = OUT / "banderole-3m-x-70cm-outlined.svg"
    outline_text(svg, outlined)

    pdf = OUT / "banderole-3m-x-70cm.pdf"
    inkscape(outlined, pdf, typ="pdf")

    pdf_edit = OUT / "banderole-3m-x-70cm-editable.pdf"
    inkscape(svg, pdf_edit, typ="pdf")

    preview = PREVIEWS / "banderole-preview.png"
    inkscape(svg, preview, typ="png", width=3000)

    hd = OUT / "banderole-3m-x-70cm-150dpi.png"
    inkscape(svg, hd, typ="png", dpi=150)

    for src in [svg, outlined, pdf, preview]:
        shutil.copy(src, ARTIFACTS / src.name)
        print("artifact", ARTIFACTS / src.name)


if __name__ == "__main__":
    main()
