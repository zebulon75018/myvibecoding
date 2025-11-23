# Exemples de Workflows

Ce fichier contient des exemples de workflows que vous pouvez créer dans l'éditeur vidéo.

## 1. Workflow Simple - Redimensionnement

```
Input → Scale (1280x720) → Output
```

**Objectif**: Redimensionner une vidéo en HD (720p)

**Paramètres**:
- Scale: width=1280, height=720

---

## 2. Workflow Créatif - Film Vintage

```
Input → Grayscale → Contrast (1.5) → Blur (0.5) → Output
```

**Objectif**: Créer un effet de film ancien

**Paramètres**:
- Grayscale: (pas de paramètres)
- Contrast: contrast=1.5
- Blur: sigma=0.5

---

## 3. Workflow de Correction - Amélioration

```
Input → Brightness (0.1) → Contrast (1.2) → Saturation (1.3) → Sharpen (1.5) → Output
```

**Objectif**: Améliorer la qualité visuelle d'une vidéo

**Paramètres**:
- Brightness: brightness=0.1
- Contrast: contrast=1.2
- Saturation: saturation=1.3
- Sharpen: amount=1.5

---

## 4. Workflow Social Media - Instagram

```
Input → Crop (1080x1080 centered) → Scale (1080x1080) → Saturation (1.4) → Output
```

**Objectif**: Préparer une vidéo pour Instagram (format carré)

**Paramètres**:
- Crop: w=1080, h=1080, x=(iw-1080)/2, y=(ih-1080)/2
- Scale: width=1080, height=1080
- Saturation: saturation=1.4

---

## 5. Workflow Intro - Fondu d'Ouverture

```
Input → Fade In (2s) → Scale (1920x1080) → Output
```

**Objectif**: Ajouter un fondu au début de la vidéo

**Paramètres**:
- Fade: type=in, duration=2
- Scale: width=1920, height=1080

---

## 6. Workflow Extraction - Clip Court

```
Input → Trim (5-15s) → Scale (1280x720) → FPS (30) → Output
```

**Objectif**: Extraire un segment de 10 secondes et optimiser

**Paramètres**:
- Trim: start=5, end=15
- Scale: width=1280, height=720
- FPS: fps=30

---

## 7. Workflow Slow Motion Dramatique

```
Input → Speed (0.5x) → Brightness (0.15) → Contrast (1.3) → Grayscale → Output
```

**Objectif**: Créer un effet slow motion dramatique en noir et blanc

**Paramètres**:
- Speed: speed=0.5
- Brightness: brightness=0.15
- Contrast: contrast=1.3
- Grayscale: (pas de paramètres)

---

## 8. Workflow Time-Lapse

```
Input → Speed (4x) → FPS (60) → Scale (1920x1080) → Sharpen (1.2) → Output
```

**Objectif**: Créer un time-lapse accéléré

**Paramètres**:
- Speed: speed=4
- FPS: fps=60
- Scale: width=1920, height=1080
- Sharpen: amount=1.2

---

## 9. Workflow Créatif - Rêve

```
Input → Blur (2.0) → Brightness (0.2) → Saturation (0.7) → Output
```

**Objectif**: Créer un effet de rêve doux

**Paramètres**:
- Blur: sigma=2.0
- Brightness: brightness=0.2
- Saturation: saturation=0.7

---

## 10. Workflow Portrait Vertical

```
Input → Crop (portrait 9:16) → Scale (1080x1920) → Rotate (0) → Output
```

**Objectif**: Convertir en format vertical pour stories/reels

**Paramètres**:
- Crop: w=(ih*9/16), h=ih, x=(iw-w)/2, y=0
- Scale: width=1080, height=1920
- Rotate: angle=0

---

## 11. Workflow Professionnel - Correction Complète

```
Input → Trim (0-30s) → Scale (1920x1080) → Brightness (0.05) → Contrast (1.15) → Saturation (1.1) → Sharpen (1.0) → FPS (30) → Output
```

**Objectif**: Pipeline de correction professionnel complet

**Paramètres**:
- Trim: start=0, end=30
- Scale: width=1920, height=1080
- Brightness: brightness=0.05
- Contrast: contrast=1.15
- Saturation: saturation=1.1
- Sharpen: amount=1.0
- FPS: fps=30

---

## 12. Workflow Rotation et Flip

```
Input → Rotate (90°) → VFlip → Scale (1920x1080) → Output
```

**Objectif**: Corriger l'orientation d'une vidéo mal filmée

**Paramètres**:
- Rotate: angle=90
- VFlip: (pas de paramètres)
- Scale: width=1920, height=1080

---

## Tips pour Créer des Workflows

### Ordre Recommandé des Filtres:

1. **Découpage/Trim** - D'abord pour réduire la quantité de données
2. **Rotation/Flip** - Corrections d'orientation
3. **Crop** - Recadrage
4. **Scale** - Redimensionnement
5. **Correction des Couleurs** (Brightness, Contrast, Saturation)
6. **Effets** (Blur, Sharpen, Grayscale)
7. **Fade** - Transitions
8. **Speed** - Modification de vitesse
9. **FPS** - Ajustement final du framerate

### Conseils de Performance:

- Utilisez Trim au début pour réduire la durée de traitement
- Scale réduit la résolution tôt pour accélérer le traitement
- Évitez les Blur trop élevés (> 5) qui ralentissent beaucoup
- Combinez plusieurs corrections de couleur en une seule si possible

### Valeurs Recommandées:

- **Brightness**: Entre -0.3 et 0.3
- **Contrast**: Entre 0.8 et 1.5
- **Saturation**: Entre 0.5 et 1.5
- **Blur**: Entre 0.5 et 3.0
- **Sharpen**: Entre 0.5 et 2.0
- **Speed**: Entre 0.25 et 4.0

---

## Comment Importer ces Workflows

Ces workflows sont des exemples conceptuels. Dans l'interface Drawflow:

1. Glissez les nœuds depuis la sidebar
2. Connectez-les dans l'ordre indiqué
3. Configurez les paramètres de chaque nœud
4. Lancez le traitement

Vous pouvez aussi sauvegarder vos workflows favoris en exportant le JSON depuis le navigateur (console développeur).
