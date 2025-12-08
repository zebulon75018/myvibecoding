# Dashboard Système en Temps Réel

Une application Flask moderne pour monitorer les performances système en temps réel avec un design élégant et des graphiques interactifs.

![](https://github.com/zebulon75018/myvibecoding/blob/main/system_dashboard/monitorsystem.png?raw=true)

## Fonctionnalités

### 📊 Métriques Système
- **Load Average** : Affichage des charges système (1, 5 et 15 minutes)
- **CPU** : Utilisation globale et par cœur, fréquence, graphiques en temps réel
- **Mémoire** : RAM et Swap avec barres de progression et graphiques historiques
- **Disques** : Informations sur toutes les partitions avec utilisation en pourcentage
- **Réseau** : Trafic entrant/sortant, paquets envoyés/reçus
- **Système** : Informations OS, uptime, architecture

### 🎨 Design Moderne
- Interface responsive avec Bootstrap 5
- Side menu collapsible avec icônes
- Graphiques interactifs avec Chart.js
- Animations fluides et design épuré
- Thème sombre pour le menu latéral

### ⚡ Temps Réel
- Mise à jour automatique toutes les 2 secondes
- Graphiques historiques (30 dernières secondes)
- API REST pour accès aux métriques

### 🔧 Macros Jinja Réutilisables
Le fichier `templates/macros.html` contient des macros pour créer facilement :
- Cartes de métriques (`metric_card`)
- Graphiques en ligne (`line_chart`)
- Graphiques en anneau (`doughnut_chart`)
- Barres de progression (`progress_bar`)
- Tableaux de données (`data_table`)
- Badges de statut (`status_badge`)
- Cartes d'information (`info_card`)

## Installation

### Prérequis
- Python 3.7+
- pip

### Étapes

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Lancer l'application**
```bash
python app.py
```

3. **Accéder au dashboard**
Ouvrez votre navigateur à l'adresse : `http://localhost:5000`

## Structure du Projet

```
system_dashboard/
│
├── app.py                      # Application Flask principale
├── requirements.txt            # Dépendances Python
│
├── templates/
│   ├── base.html              # Template de base avec sidemenu
│   ├── dashboard.html         # Page du dashboard
│   └── macros.html            # Macros Jinja réutilisables
│
└── static/
    ├── css/
    │   └── style.css          # Styles personnalisés
    └── js/
        └── dashboard.js       # JavaScript pour le temps réel
```

## API Endpoints

L'application expose plusieurs endpoints API REST :

- `GET /api/metrics` - Toutes les métriques système
- `GET /api/cpu` - Informations CPU uniquement
- `GET /api/memory` - Informations mémoire uniquement
- `GET /api/load` - Load average uniquement

### Exemple de réponse `/api/metrics`
```json
{
  "cpu": {
    "percent": 25.5,
    "count": 8,
    "freq": 2400.0,
    "per_cpu": [23.1, 27.8, ...]
  },
  "memory": {
    "total": 16.0,
    "used": 8.5,
    "percent": 53.2,
    ...
  },
  "load": {
    "load1": 1.23,
    "load5": 1.45,
    "load15": 1.67
  },
  ...
}
```

## Utilisation des Macros

### Exemple : Ajouter une nouvelle métrique

```jinja
{% from "macros.html" import metric_card %}

{{ metric_card(
    title="Température CPU",
    value="65",
    unit="°C",
    icon="thermometer-half",
    color="warning",
    id="cpu-temp"
) }}
```

### Exemple : Ajouter un nouveau graphique

```jinja
{% from "macros.html" import line_chart %}

{{ line_chart(
    title="Utilisation Réseau",
    chart_id="networkUsageChart",
    height="300"
) }}
```

Puis dans le JavaScript :
```javascript
const ctx = document.getElementById('networkUsageChart');
const chart = new Chart(ctx, {
    type: 'line',
    data: { ... },
    options: { ... }
});
```

## Personnalisation

### Modifier l'intervalle de mise à jour
Dans `static/js/dashboard.js`, changez la ligne :
```javascript
setInterval(updateMetrics, 2000); // 2000ms = 2 secondes
```

### Modifier les couleurs du thème
Dans `static/css/style.css`, modifiez les variables CSS :
```css
:root {
    --primary-color: #4A90E2;
    --sidebar-width: 260px;
    ...
}
```

### Ajouter une nouvelle métrique
1. Ajouter une fonction dans `app.py` pour récupérer les données
2. Ajouter un endpoint API
3. Créer une section dans `dashboard.html` avec les macros
4. Ajouter la logique de mise à jour dans `dashboard.js`

## Technologies Utilisées

- **Backend** : Flask (Python)
- **Monitoring** : psutil
- **Frontend** : Bootstrap 5, Chart.js
- **Icons** : Bootstrap Icons
- **Template Engine** : Jinja2

## Compatibilité

- ✅ Linux (toutes les fonctionnalités)
- ✅ Windows (load average retourne 0)
- ✅ macOS (toutes les fonctionnalités)

## Notes

- Les métriques réseau affichent les totaux cumulés depuis le démarrage
- Le load average n'est pas disponible sur Windows
- Certaines partitions peuvent nécessiter des permissions root pour être lues

## Licence

Libre d'utilisation et de modification.
