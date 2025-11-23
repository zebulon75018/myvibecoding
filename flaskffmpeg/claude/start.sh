#!/bin/bash

echo "=========================================="
echo "  Éditeur Vidéo FFmpeg avec Drawflow"
echo "=========================================="
echo ""

# Vérifier si FFmpeg est installé
if ! command -v ffmpeg &> /dev/null
then
    echo "❌ ERREUR: FFmpeg n'est pas installé!"
    echo ""
    echo "Veuillez installer FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: télécharger depuis https://ffmpeg.org/download.html"
    exit 1
fi

echo "✅ FFmpeg détecté: $(ffmpeg -version | head -n 1)"
echo ""

# Vérifier si venv existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer venv
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Démarrage de l'application..."
echo ""
echo "L'application sera accessible à: http://localhost:5000"
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Lancer l'application
python app.py
