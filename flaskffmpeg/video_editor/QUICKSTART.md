# Guide de Démarrage Rapide 🚀

Bienvenue dans l'éditeur vidéo FFmpeg avec Drawflow ! Ce guide vous aidera à créer votre première vidéo en quelques minutes.

## Installation en 3 Étapes

### 1. Installer FFmpeg

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Télécharger depuis https://ffmpeg.org/download.html et ajouter au PATH

Vérifier l'installation:
```bash
ffmpeg -version
```

### 2. Installer les Dépendances Python

```bash
cd video_editor
pip install -r requirements.txt
```

### 3. Lancer l'Application

**Option A - Script automatique:**
```bash
./start.sh
```

**Option B - Manuellement:**
```bash
python app.py
```

Ouvrir votre navigateur: **http://localhost:5000**

---

## Votre Première Vidéo en 5 Minutes

### Étape 1: Générer une Vidéo de Test (Optionnel)

Si vous n'avez pas de vidéo, créez-en une:
```bash
python generate_test_video.py
```

Choisissez l'option 1 pour une vidéo de test standard.

### Étape 2: Charger la Vidéo

1. Cliquez sur **"Choisir un fichier"**
2. Sélectionnez votre vidéo (ou `test_video.mp4`)
3. Les informations s'affichent (résolution, durée, codec)

### Étape 3: Créer Votre Workflow

**Workflow Simple - Redimensionner:**

1. Trouvez le nœud **"Input Vidéo"** (déjà présent à gauche)
2. Glissez un nœud **"Scale"** depuis la sidebar
3. Configurez: width=1280, height=720
4. Trouvez le nœud **"Output Vidéo"** (à droite)

### Étape 4: Connecter les Nœuds

1. Cliquez sur la **sortie** (point à droite) du nœud Input
2. Glissez jusqu'à l'**entrée** (point à gauche) du nœud Scale
3. Faites de même de Scale vers Output

Vous devriez voir: `Input → Scale → Output`

### Étape 5: Traiter !

1. Cliquez sur **"Traiter la vidéo"** (bouton vert)
2. Attendez... (une barre de progression apparaît)
3. Téléchargez votre vidéo !

🎉 **Félicitations !** Vous avez créé votre première vidéo traitée !

---

## Workflows Populaires pour Commencer

### 📱 Pour Instagram (Format Carré)
```
Input → Crop (1080x1080) → Saturation (1.4) → Output
```

### 🎬 Film Vintage
```
Input → Grayscale → Contrast (1.5) → Output
```

### ⚡ Time-Lapse Rapide
```
Input → Speed (4x) → FPS (60) → Output
```

### 🌟 Amélioration Automatique
```
Input → Brightness (0.1) → Contrast (1.2) → Sharpen (1.5) → Output
```

---

## Interface Utilisateur

### Zone de Gauche (Sidebar)
- 📤 **Section Upload**: Charger vos vidéos
- 🎨 **Filtres**: Tous les effets disponibles
  - Cliquez pour ajouter
  - Glissez-déposez vers la zone centrale

### Zone Centrale (Editeur)
- 🎯 **Canvas Drawflow**: Créez votre pipeline visuel
- 🔗 **Connexions**: Reliez les nœuds entre eux
- ⚙️ **Nœuds**: Chaque nœud = un filtre avec ses paramètres

### Zone du Haut (Header)
- 🗑️ **Bouton Effacer**: Recommencer à zéro
- ▶️ **Bouton Traiter**: Lancer le traitement

---

## Raccourcis et Astuces

### Navigation
- **Clic gauche + glisser**: Déplacer un nœud
- **Clic droit + glisser**: Déplacer la vue
- **Molette**: Zoom (si activé)

### Édition
- **Cliquer sur un nœud**: Le sélectionner
- **Double-cliquer**: Voir les détails
- **Supprimer**: Clic droit → Supprimer (ou sélectionner + Suppr)

### Connexions
- **Clic sur sortie → entrée**: Créer une connexion
- **Clic sur connexion**: La sélectionner
- **Supprimer une connexion**: Cliquer dessus puis Suppr

---

## Filtres les Plus Utilisés

| Filtre | Usage | Paramètres Clés |
|--------|-------|----------------|
| **Scale** | Redimensionner | width, height |
| **Crop** | Recadrer | w, h, x, y |
| **Brightness** | Luminosité | -1 à 1 |
| **Contrast** | Contraste | 0 à 3 |
| **Saturation** | Couleurs | 0 à 3 |
| **Blur** | Flou | 0 à 10 |
| **Sharpen** | Netteté | 0 à 5 |
| **Speed** | Vitesse | 0.25 à 4 |
| **Trim** | Découper | start, end (secondes) |
| **Fade** | Fondu | in/out, duration |

---

## Résolution de Problèmes Courants

### ❌ "FFmpeg not found"
**Solution**: Installer FFmpeg et vérifier avec `ffmpeg -version`

### ❌ "Aucun fichier fourni"
**Solution**: Cliquer sur "Choisir un fichier" et sélectionner une vidéo

### ❌ "Veuillez connecter au moins un filtre"
**Solution**: Connecter Input → (filtres) → Output

### ❌ Traitement très lent
**Solutions**:
- Utiliser Trim pour traiter seulement une partie
- Réduire la résolution avec Scale en début de pipeline
- Éviter Blur avec sigma > 3

### ❌ Vidéo de mauvaise qualité
**Solutions**:
- Augmenter légèrement Sharpen (1.0-1.5)
- Ajuster Brightness et Contrast
- Vérifier que Scale n'agrandit pas trop l'image

---

## Exemples de Commandes API (Avancé)

### Upload
```python
import requests

with open('video.mp4', 'rb') as f:
    r = requests.post('http://localhost:5000/upload', files={'video': f})
    print(r.json())
```

### Obtenir les Filtres
```python
r = requests.get('http://localhost:5000/filters')
print(r.json())
```

Voir `example_api_usage.py` pour plus d'exemples.

---

## Prochaines Étapes

1. ✅ Essayez les workflows dans `WORKFLOWS.md`
2. 📖 Lisez le `README.md` complet
3. 🎨 Expérimentez avec différentes combinaisons de filtres
4. 🚀 Créez vos propres workflows personnalisés
5. 💡 Consultez la documentation FFmpeg pour des filtres avancés

---

## Support

- **Documentation FFmpeg**: https://ffmpeg.org/documentation.html
- **Drawflow GitHub**: https://github.com/jerosoler/Drawflow
- **ffmpeg-python Docs**: https://github.com/kkroening/ffmpeg-python

---

## Bon à Savoir

- ⏱️ Le traitement peut prendre du temps selon:
  - La durée de la vidéo
  - La résolution
  - Le nombre de filtres
  - La complexité des filtres

- 💾 Les fichiers sont stockés dans:
  - `uploads/` - Vidéos uploadées
  - `outputs/` - Vidéos traitées

- 🔒 Limite: 500 MB par fichier

- 📁 Formats supportés: MP4, AVI, MOV, MKV, FLV, WMV

---

**Amusez-vous bien ! 🎬✨**
