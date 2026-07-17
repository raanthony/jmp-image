# Banderole vectorielle — Fitoriana Filazantsara Lehibe

Impression HD **3,00 m × 0,70 m** pour Fiangonana Jesosy Mpamonjy Morafeno Ambositra (6–9 Aogositra 2026).

## Fichiers à donner à l’imprimeur

| Fichier | Usage |
|---|---|
| `banner/banderole-3m-x-70cm.pdf` | **Recommandé** — PDF vectoriel, textes en courbes |
| `banner/banderole-3m-x-70cm-outlined.svg` | SVG vectoriel, textes convertis en chemins |
| `banner/banderole-3m-x-70cm.svg` | SVG éditable (textes modifiables) |
| `banner/banderole-3m-x-70cm-150dpi.png` | Aperçu / BAT raster à 150 dpi |

## Spécifications d’impression

- Format fini : **3000 × 700 mm**
- Mode couleur : RGB (conversion CMJN chez l’imprimeur)
- Fond perdu : non inclus — demander +20 mm tout autour si besoin
- Résolution raster équivalente : 150 dpi (standard banderole vue à distance)

## Régénérer

```bash
python3 scripts/build_banner.py
```

Polices utilisées : Montserrat, Open Sans, Dancing Script, Great Vibes (`fonts/`).

## Note

Les horaires et lieux des 4 jours dans le programme sont à **vérifier / ajuster** si votre flyer source diffère (modifier `days` dans `scripts/build_banner.py` puis relancer le script).
