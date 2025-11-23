# Éditeur Vidéo FFmpeg avec Drawflow

Une application web interactive pour traiter des vidéos en utilisant FFmpeg avec une interface visuelle basée sur Drawflow.

## Fonctionnalités

- 🎬 Interface visuelle pour créer des pipelines de traitement vidéo
- 🔧 Multiples filtres FFmpeg disponibles (15+ filtres)
- 📊 Connexion visuelle des filtres via drag & drop
- 🎨 Interface moderne et intuitive
- ⚡ Traitement en temps réel avec FFmpeg

## Filtres disponibles

- **Scale** : Redimensionner la vidéo
- **Crop** : Rogner la vidéo
- **Rotate** : Rotation de la vidéo
- **Flip** : Miroir horizontal/vertical
- **Brightness** : Ajuster la luminosité
- **Contrast** : Ajuster le contraste
- **Saturation** : Ajuster la saturation
- **Blur** : Ajouter un flou
- **Sharpen** : Augmenter la netteté
- **Fade** : Effet de fondu
- **Grayscale** : Noir et blanc
- **Speed** : Changer la vitesse
- **FPS** : Modifier le framerate
- **Trim** : Découper la vidéo

## Prérequis

- Python 3.8 ou supérieur
- FFmpeg installé sur le système

### Installation de FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Télécharger depuis https://ffmpeg.org/download.html

## Installation

1. Cloner ou télécharger le projet

2. Créer un environnement virtuel (recommandé):
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancer l'application:
```bash
python app.py
```

2. Ouvrir votre navigateur à l'adresse:
```
http://localhost:5000
```

3. Utiliser l'interface:
   - Cliquez sur "Choisir un fichier" pour charger une vidéo
   - Glissez-déposez des filtres depuis la sidebar vers la zone de travail
   - Connectez les nœuds entre eux (sortie → entrée)
   - Configurez les paramètres de chaque filtre
   - Cliquez sur "Traiter la vidéo" pour lancer le processus
   - Téléchargez le résultat

## Structure du projet

```
video_editor/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── templates/
│   └── index.html        # Template HTML principal
├── static/
│   ├── css/
│   │   └── style.css     # Styles CSS
│   └── js/
│       └── app.js        # Logique JavaScript/Drawflow
├── uploads/              # Dossier pour les vidéos uploadées
└── outputs/              # Dossier pour les vidéos traitées
```

## Architecture

### Backend (Flask)
- Gestion de l'upload de vidéos
- Traitement des vidéos avec ffmpeg-python
- API REST pour l'interaction avec le frontend

### Frontend (Drawflow)
- Interface visuelle pour créer des workflows
- Drag & drop des filtres
- Configuration dynamique des paramètres
- Prévisualisation des filtres disponibles

## Exemples de workflow

### Exemple 1 : Redimensionner et ajouter un effet
```
Input → Scale (1280x720) → Brightness (+0.2) → Output
```

### Exemple 2 : Créer une vidéo noir et blanc ralentie
```
Input → Grayscale → Speed (0.5x) → Output
```

### Exemple 3 : Découper et rogner
```
Input → Trim (0-10s) → Crop (640x480) → Output
```

## API Endpoints

### POST /upload
Upload une vidéo
- Body: FormData avec le fichier vidéo
- Retour: Informations sur la vidéo (résolution, durée, codec)

### POST /process
Traiter une vidéo avec le workflow
- Body: JSON avec le fichier d'entrée et le workflow Drawflow
- Retour: URL de téléchargement de la vidéo traitée

### GET /filters
Obtenir la liste des filtres disponibles
- Retour: JSON avec tous les filtres et leurs paramètres

### GET /download/<filename>
Télécharger une vidéo traitée

## Technologies utilisées

- **Backend**: Flask (Python)
- **Traitement vidéo**: FFmpeg, ffmpeg-python
- **Frontend**: Drawflow.js
- **UI**: HTML5, CSS3, JavaScript ES6+
- **Icons**: Font Awesome

## Limitations

- Taille maximale de fichier: 500MB
- Formats supportés: MP4, AVI, MOV, MKV, FLV, WMV
- Le traitement peut prendre du temps selon la complexité du workflow

## Conseils d'utilisation

1. Commencez toujours par le nœud "Entrée Vidéo"
2. Terminez toujours par le nœud "Sortie Vidéo"
3. Connectez les nœuds dans l'ordre logique de traitement
4. Testez avec de petites vidéos d'abord
5. Les filtres sont appliqués dans l'ordre des connexions

## Dépannage

**Erreur "FFmpeg not found":**
- Vérifiez que FFmpeg est installé: `ffmpeg -version`
- Ajoutez FFmpeg au PATH système

**Erreur lors du traitement:**
- Vérifiez que tous les nœuds sont connectés
- Vérifiez les valeurs des paramètres (pas de valeurs négatives invalides)
- Consultez les logs Flask pour plus de détails

**Upload échoue:**
- Vérifiez la taille du fichier (< 500MB)
- Vérifiez le format du fichier

## Développement futur

- [ ] Prévisualisation en temps réel
- [ ] Support de plus de filtres FFmpeg
- [ ] Sauvegarde/chargement de workflows
- [ ] Support audio
- [ ] Traitement par batch
- [ ] Support de plusieurs entrées (overlay, concat)

## Licence

MIT

## Auteur

Créé avec ❤️ en utilisant Flask, FFmpeg et Drawflow
