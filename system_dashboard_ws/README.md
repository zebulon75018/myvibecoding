# Dashboard Système avec WebSockets (Linux)

Une application Flask moderne pour monitorer les performances système en temps réel avec **WebSockets** au lieu d'appels AJAX. Optimisée pour Linux.

## 🚀 Avantages des WebSockets

### Par rapport aux appels AJAX/Polling :
- ✅ **Connexion persistante** - Une seule connexion bidirectionnelle au lieu de multiples requêtes HTTP
- ✅ **Latence réduite** - Pas de handshake HTTP répété, mise à jour instantanée
- ✅ **Charge serveur réduite** - Pas de création/destruction de connexions constantes
- ✅ **Push en temps réel** - Le serveur envoie les données dès qu'elles sont prêtes
- ✅ **Efficacité réseau** - Moins d'overhead de protocole (pas de headers HTTP répétés)
- ✅ **Scalabilité** - Meilleure gestion de multiples clients simultanés

### Comparaison technique :

**AJAX Polling (version précédente) :**
```
Client → HTTP Request → Serveur
Client ← HTTP Response ← Serveur
[Attente 2 secondes]
Client → HTTP Request → Serveur
... (répété indéfiniment)
```

**WebSocket (cette version) :**
```
Client ↔ WebSocket Handshake ↔ Serveur
[Connexion maintenue]
Client ← Push Data ← Serveur
Client ← Push Data ← Serveur
... (automatique, pas d'attente)
```

## 🎯 Fonctionnalités

- **Load Average** : Surveillance de la charge système (Linux)
- **CPU** : Utilisation globale et par cœur + graphiques temps réel
- **Mémoire** : RAM et Swap avec historique
- **Disques** : État de toutes les partitions
- **Réseau** : Trafic entrant/sortant en temps réel
- **Système** : Informations OS, uptime, etc.

## 📊 Technologies

- **Backend** : Flask + Flask-SocketIO
- **WebSocket** : Socket.IO (protocole WebSocket avec fallback)
- **Monitoring** : psutil
- **Frontend** : Bootstrap 5, Chart.js
- **Asyncio** : Threading pour émission temps réel

## 🔧 Installation

### Prérequis
- Python 3.7+
- Linux (Ubuntu, Debian, CentOS, etc.)

### Installation rapide

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

Ou utilisez le script de démarrage :
```bash
chmod +x start.sh
./start.sh
```

### Installation avec environnement virtuel (recommandé)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 🌐 Accès

Ouvrez votre navigateur à : **http://localhost:5000**

Vous devriez voir l'indicateur "WebSocket Actif" en vert dans la barre de navigation.

## 🏗️ Architecture WebSocket

### Serveur (app.py)

```python
# Thread en arrière-plan qui émet les métriques
def background_metrics_updater():
    while True:
        metrics = get_all_metrics()
        socketio.emit('metrics_update', metrics)
        time.sleep(2)

# Connexion client
@socketio.on('connect')
def handle_connect():
    # Démarre le thread si pas déjà actif
    # Envoie immédiatement les métriques
```

### Client (dashboard.js)

```javascript
// Initialisation Socket.IO
socket = io();

// Réception des métriques
socket.on('metrics_update', function(data) {
    updateMetricsFromSocket(data);
});

// Gestion des événements
socket.on('connect', ...);
socket.on('disconnect', ...);
```

## 📁 Structure

```
system_dashboard_ws/
├── app.py                      # Flask + SocketIO
├── requirements.txt            # Dépendances
├── start.sh                    # Script démarrage
├── README.md                   # Ce fichier
│
├── templates/
│   ├── base.html              # Template base + Socket.IO
│   ├── dashboard.html         # Dashboard principal
│   └── macros.html            # Macros Jinja
│
└── static/
    ├── css/
    │   └── style.css          # CSS personnalisé
    └── js/
        └── dashboard.js       # Socket.IO client
```

## 🔍 Monitoring de la Connexion

L'application affiche deux indicateurs de connexion WebSocket :

1. **Dans le sidebar** : Badge "Connecté/Déconnecté"
2. **Dans la navbar** : Badge "WebSocket Actif/Inactif"

Ces indicateurs changent automatiquement selon l'état de la connexion.

## ⚙️ Configuration

### Modifier l'intervalle d'émission

Dans `app.py`, ligne du thread :
```python
time.sleep(2)  # Émettre toutes les 2 secondes
```

### Modifier le port

Dans `app.py`, dernière ligne :
```python
socketio.run(app, host='0.0.0.0', port=8080)  # Utiliser le port 8080
```

### Activer le mode production

```python
socketio.run(app, debug=False, host='0.0.0.0', port=5000)
```

## 🛠️ Macros Jinja

Les mêmes macros que la version AJAX sont disponibles :

```jinja
{% from "macros.html" import metric_card, line_chart %}

{{ metric_card("CPU", "45", "%", "cpu", "primary") }}
{{ line_chart("Historique", "myChart") }}
```

Voir `templates/macros.html` pour la liste complète.

## 🐛 Débogage

### Vérifier la connexion WebSocket

Ouvrez la console développeur du navigateur (F12) :
```
WebSocket connecté!
Métriques reçues via WebSocket
```

### Test manuel

Dans la console :
```javascript
socket.emit('request_metrics');
```

### Logs serveur

Le serveur affiche :
```
Client connecté
Client déconnecté
```

## 🚀 Déploiement Production

### Avec Gunicorn + Eventlet

```bash
pip install gunicorn eventlet
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

**Important** : Utilisez `-w 1` (un seul worker) avec eventlet pour WebSockets.

### Avec systemd

Créez `/etc/systemd/system/dashboard.service` :

```ini
[Unit]
Description=Dashboard Système WebSocket
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/system_dashboard_ws
Environment="PATH=/opt/system_dashboard_ws/venv/bin"
ExecStart=/opt/system_dashboard_ws/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Puis :
```bash
sudo systemctl enable dashboard
sudo systemctl start dashboard
```

## 📊 Comparaison Performances

| Métrique | AJAX Polling | WebSocket |
|----------|--------------|-----------|
| Connexions/min | 30 | 1 |
| Headers HTTP/min | ~60KB | ~1KB |
| Latence moyenne | 50-200ms | 1-10ms |
| CPU serveur | Moyen | Faible |
| Bande passante | ~1MB/min | ~100KB/min |

## 🔐 Sécurité

### Authentification (optionnel)

Pour ajouter de l'authentification :

```python
from flask_socketio import disconnect

@socketio.on('connect')
def handle_connect(auth):
    if not verify_auth(auth):
        disconnect()
```

### CORS

Modifier dans `app.py` :
```python
socketio = SocketIO(app, cors_allowed_origins=["https://votredomaine.com"])
```

## ❓ FAQ

**Q: Pourquoi utiliser threading au lieu d'async/await ?**  
R: Flask-SocketIO avec eventlet gère déjà l'async de manière efficace. Le threading est simple et fonctionne bien pour ce cas d'usage.

**Q: Peut-on avoir plusieurs clients connectés ?**  
R: Oui ! Le serveur diffuse (broadcast) les métriques à tous les clients connectés.

**Q: Que se passe-t-il si la connexion est perdue ?**  
R: Socket.IO reconnecte automatiquement et les indicateurs changent de couleur.

**Q: Ça fonctionne sur Windows ?**  
R: Cette version est optimisée pour Linux. Certaines métriques (load average) ne sont pas disponibles sur Windows.

## 📚 Ressources

- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Documentation](https://socket.io/docs/)
- [psutil Documentation](https://psutil.readthedocs.io/)

## 📝 Licence

Libre d'utilisation et de modification.

---

**Note** : Cette version utilise WebSockets pour une expérience temps réel optimale. Pour une version compatible tous systèmes avec AJAX, voir `system_dashboard/`.
