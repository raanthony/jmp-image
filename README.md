# Banderole vectorielle — Fitoriana Filazantsara Lehibe

Recréation du flyer original pour impression HD **3,00 m × 0,70 m**  
(Fiangonana Jesosy Mpamonjy Morafeno Ambositra — 6–9 Aogositra 2026).

## Fichiers à donner à l’imprimeur

| Fichier | Usage |
|---|---|
| `banner/banderole-3m-x-70cm.pdf` | **Recommandé** — PDF vectoriel, textes en courbes |
| `banner/banderole-3m-x-70cm-outlined.svg` | SVG vectoriel sans dépendance de polices |
| `banner/banderole-3m-x-70cm.svg` | SVG éditable |
| `banner/banderole-3m-x-70cm-150dpi.png` | Aperçu / BAT raster 150 dpi |

## Contenu repris du flyer

- Barre d’en-tête, logo église, titre FITORIANA FILAZANTSARA / LEHIBE  
- Citation Marka 16:15 + photo foule / coucher de soleil  
- Invitation, dates 6–7–8–9 Aogositra 2026, 3 points (famonjena / fanasitranana / fiainana)  
- Programme 4 jours (Alakamisy → Alahady)  
- Appel cursive + contact Mpitandrina RANDRIANARIZANANY Lovasoa Fenomanana  

## Spécifications

- Format fini : **3000 × 700 mm**
- Couleurs : RGB (CMJN chez l’imprimeur)
- Fond perdu : non inclus (+20 mm si besoin)

## Régénérer

```bash
python3 scripts/build_banner.py
```

Polices : Montserrat, Open Sans, Dancing Script, Great Vibes (`fonts/`).  
Photo inset : `assets/crowd-sunset-wide.jpg`.

## À vérifier

Si les **horaires / lieux** des 4 jours diffèrent du flyer papier, modifier `days` dans `scripts/build_banner.py` puis relancer.
