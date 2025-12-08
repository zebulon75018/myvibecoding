# Guide de Personnalisation - Dashboard Système

## 🎨 Personnalisation du Design

### Couleurs du Thème
Modifiez les variables CSS dans `static/css/style.css` :

```css
:root {
    --sidebar-width: 260px;                    /* Largeur du menu latéral */
    --sidebar-collapsed-width: 70px;          /* Largeur menu réduit */
    --primary-color: #4A90E2;                 /* Couleur principale */
    --secondary-color: #6c757d;               /* Couleur secondaire */
    --success-color: #28a745;                 /* Vert pour succès */
    --danger-color: #dc3545;                  /* Rouge pour erreurs */
    --warning-color: #ffc107;                 /* Orange pour alertes */
    --info-color: #17a2b8;                    /* Bleu pour info */
    --dark-bg: #2c3e50;                       /* Fond sombre */
    --light-bg: #f8f9fa;                      /* Fond clair */
}
```

### Modifier la Largeur du Sidebar
```css
--sidebar-width: 300px;  /* Plus large */
--sidebar-width: 200px;  /* Plus étroit */
```

### Changer le Gradient du Sidebar
```css
.sidebar {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
```

## 📊 Ajout de Nouvelles Métriques

### Étape 1 : Créer la Fonction de Collecte (app.py)

```python
def get_temperature_info():
    """Récupère les températures du système"""
    try:
        temps = psutil.sensors_temperatures()
        return {
            'cpu_temp': temps['coretemp'][0].current if 'coretemp' in temps else 0,
            'critical': temps['coretemp'][0].critical if 'coretemp' in temps else 0
        }
    except:
        return {'cpu_temp': 0, 'critical': 0}
```

### Étape 2 : Ajouter l'Endpoint API (app.py)

```python
@app.route('/api/temperature')
def get_temperature():
    """API pour récupérer les températures"""
    return jsonify(get_temperature_info())

# Ajouter aux métriques complètes
@app.route('/api/metrics')
def get_metrics():
    return jsonify({
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'temperature': get_temperature_info(),  # Nouvelle métrique
        # ...
    })
```

### Étape 3 : Créer l'Interface (dashboard.html)

```jinja
{% from "macros.html" import metric_card, line_chart %}

<div class="row mb-4" id="temperature">
    <div class="col-12">
        <h2><i class="bi bi-thermometer"></i> Températures</h2>
    </div>
    
    {{ metric_card("Temp. CPU", "0", "°C", "thermometer-half", "warning", "cpu-temp") }}
    
    <div class="col-md-6">
        {{ line_chart("Historique Température CPU", "tempChart") }}
    </div>
</div>
```

### Étape 4 : Implémenter la Mise à Jour JS (dashboard.js)

```javascript
// Variables globales
let tempChart;
let tempHistory = [];

// Dans initCharts()
function initCharts() {
    // ...autres graphiques...
    
    const tempCtx = document.getElementById('tempChart');
    if (tempCtx) {
        tempChart = new Chart(tempCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Température CPU (°C)',
                    data: [],
                    borderColor: 'rgba(255, 193, 7, 1)',
                    backgroundColor: 'rgba(255, 193, 7, 0.2)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value + '°C';
                            }
                        }
                    }
                }
            }
        });
    }
}

// Dans updateMetrics()
async function updateMetrics() {
    const response = await fetch('/api/metrics');
    const data = await response.json();
    
    // Mise à jour température
    updateTemperature(data.temperature);
    
    // Mise à jour du graphique
    tempHistory.push(data.temperature.cpu_temp);
    if (tempHistory.length > maxDataPoints) {
        tempHistory.shift();
    }
    
    if (tempChart) {
        tempChart.data.labels.push(timeLabel);
        tempChart.data.datasets[0].data = tempHistory;
        if (tempChart.data.labels.length > maxDataPoints) {
            tempChart.data.labels.shift();
        }
        tempChart.update('none');
    }
}

function updateTemperature(temp) {
    document.getElementById('cpu-temp').textContent = temp.cpu_temp.toFixed(1) + '°C';
}
```

## 🔧 Utilisation Avancée des Macros

### Créer une Macro Personnalisée (macros.html)

```jinja
{# Macro pour une carte avec graphique sparkline #}
{% macro sparkline_card(title, current_value, unit, data_points, color="primary") %}
<div class="col-md-3 mb-4">
    <div class="card">
        <div class="card-body">
            <h6 class="text-muted">{{ title }}</h6>
            <h3>{{ current_value }}{{ unit }}</h3>
            <canvas id="sparkline-{{ title|lower|replace(' ', '-') }}" 
                    height="50"></canvas>
        </div>
    </div>
</div>
{% endmacro %}
```

### Utiliser la Macro

```jinja
{{ sparkline_card("CPU Usage", "45", "%", [30,35,40,45], "primary") }}
```

## ⚙️ Configuration Avancée

### Changer l'Intervalle de Rafraîchissement

Dans `dashboard.js` :
```javascript
// Mettre à jour toutes les X millisecondes
setInterval(updateMetrics, 1000);  // 1 seconde
setInterval(updateMetrics, 5000);  // 5 secondes
```

### Modifier le Nombre de Points d'Historique

```javascript
const maxDataPoints = 60; // 60 secondes au lieu de 30
```

### Ajouter un Élément au Menu Latéral

Dans `base.html` :
```html
<nav class="sidebar-nav">
    <!-- ...éléments existants... -->
    
    <a href="#custom" class="nav-link">
        <i class="bi bi-star"></i>
        <span>Ma Section</span>
    </a>
</nav>
```

## 📱 Responsive Design

### Points de Rupture Bootstrap

```scss
// Extra small devices (portrait phones, less than 576px)
// No media query for `xs` since this is the default in Bootstrap

// Small devices (landscape phones, 576px and up)
@media (min-width: 576px) { ... }

// Medium devices (tablets, 768px and up)
@media (min-width: 768px) { ... }

// Large devices (desktops, 992px and up)
@media (min-width: 992px) { ... }

// Extra large devices (large desktops, 1200px and up)
@media (min-width: 1200px) { ... }
```

### Adapter une Section pour Mobile

```jinja
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">
        {# 12 colonnes sur mobile, 6 sur tablette, 4 sur desktop #}
    </div>
</div>
```

## 🎯 Exemples de Métriques Personnalisées

### 1. Processus les Plus Gourmands

```python
def get_top_processes():
    """Top 5 processus par utilisation CPU"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return sorted(processes, key=lambda x: x['cpu_percent'], 
                  reverse=True)[:5]
```

### 2. Utilisation des Ports Réseau

```python
def get_network_connections():
    """Connexions réseau actives"""
    connections = psutil.net_connections()
    return {
        'total': len(connections),
        'established': len([c for c in connections if c.status == 'ESTABLISHED']),
        'listening': len([c for c in connections if c.status == 'LISTEN'])
    }
```

### 3. Informations Batterie (Laptops)

```python
def get_battery_info():
    """État de la batterie"""
    try:
        battery = psutil.sensors_battery()
        return {
            'percent': battery.percent,
            'plugged': battery.power_plugged,
            'time_left': battery.secsleft / 60 if battery.secsleft != -1 else -1
        }
    except:
        return None
```

## 🚀 Optimisations de Performance

### 1. Cache des Métriques Lentes

```python
from functools import lru_cache
import time

@lru_cache(maxsize=1)
def get_system_info_cached():
    return get_system_info(), time.time()

@app.route('/api/system')
def get_system_cached():
    info, timestamp = get_system_info_cached()
    # Cache valide 60 secondes
    if time.time() - timestamp > 60:
        get_system_info_cached.cache_clear()
    return jsonify(info)
```

### 2. Compression des Réponses API

```python
from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
```

### 3. Limiter les Appels API

Dans `dashboard.js` :
```javascript
let updateInProgress = false;

async function updateMetrics() {
    if (updateInProgress) return;
    updateInProgress = true;
    
    try {
        // ...mise à jour...
    } finally {
        updateInProgress = false;
    }
}
```

## 🔐 Sécurité

### Ajouter une Authentification Simple

```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("password123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('dashboard.html')
```

## 📦 Déploiement Production

### Avec Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Avec Docker

Créez un `Dockerfile` :
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🐛 Débogage

### Activer les Logs Détaillés

```python
import logging

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
```

### Tester les API Endpoints

```bash
curl http://localhost:5000/api/metrics | jq
curl http://localhost:5000/api/cpu | jq
```

---

Pour plus d'informations, consultez la documentation officielle :
- Flask : https://flask.palletsprojects.com/
- Chart.js : https://www.chartjs.org/
- Bootstrap : https://getbootstrap.com/
- psutil : https://psutil.readthedocs.io/
