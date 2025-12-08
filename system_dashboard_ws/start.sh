#!/bin/bash

echo "=========================================="
echo "  Dashboard Système - Version WebSocket"
echo "=========================================="
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Python 3 détecté"

# Vérifier si on est sur Linux
if [ "$(uname)" != "Linux" ]; then
    echo "⚠️  ATTENTION: Cette version est optimisée pour Linux"
    echo "   Certaines fonctionnalités peuvent ne pas fonctionner correctement"
fi

# Créer un environnement virtuel (optionnel)
read -p "Voulez-vous créer un environnement virtuel ? (recommandé) [o/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances (Flask-SocketIO, psutil, eventlet)..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées avec succès"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

# Lancer l'application
echo ""
echo "=========================================="
echo "  Démarrage du Dashboard WebSocket"
echo "=========================================="
echo ""
echo "🚀 L'application sera accessible à : http://localhost:5000"
echo "   WebSocket actif pour les mises à jour en temps réel"
echo "   Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""
sleep 2

python3 app.py
