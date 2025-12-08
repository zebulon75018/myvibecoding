# 🚀 Démarrage Rapide

## Installation en 3 étapes

### Option 1 : Script Automatique

**Linux/Mac :**
```bash
chmod +x start.sh
./start.sh
```

**Windows :**
```bash
start.bat
```

### Option 2 : Installation Manuelle

1. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

2. **Lancer l'application**
   ```bash
   python app.py
   ```

3. **Ouvrir dans le navigateur**
   ```
   http://localhost:5000
   ```

## ✨ Fonctionnalités Principales

- ✅ **Load Average** - Surveillance de la charge système
- ✅ **CPU** - Utilisation globale et par cœur + graphiques
- ✅ **Mémoire** - RAM et Swap en temps réel
- ✅ **Disques** - État de toutes les partitions
- ✅ **Réseau** - Trafic entrant/sortant
- ✅ **Système** - Infos OS et uptime

## 🎨 Macros Jinja Disponibles

Toutes les macros sont dans `templates/macros.html` :

```jinja
{% from "macros.html" import metric_card, line_chart %}

{{ metric_card("Titre", "Valeur", "Unité", "icone", "couleur", "id") }}
{{ line_chart("Titre du graphique", "chartId", "300") }}
{{ doughnut_chart("Titre", "chartId") }}
{{ progress_bar("Label", 75, "couleur", "id") }}
```

## 📖 Documentation Complète

- `README.md` - Documentation générale
- `CUSTOMIZATION.md` - Guide de personnalisation détaillé
- `templates/custom_example.html` - Exemples d'utilisation

## 🔧 Configuration Rapide

### Changer l'intervalle de mise à jour
Dans `static/js/dashboard.js`, ligne finale :
```javascript
setInterval(updateMetrics, 2000); // 2000ms = 2 secondes
```

### Modifier les couleurs
Dans `static/css/style.css` :
```css
:root {
    --primary-color: #4A90E2;  /* Votre couleur */
}
```

### Ajouter une métrique
1. Fonction dans `app.py`
2. Endpoint API
3. Section dans `dashboard.html`
4. Logique JS dans `dashboard.js`

## 🆘 Problèmes Courants

**Port 5000 déjà utilisé ?**
Dans `app.py`, changez :
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

**Permission refusée sur Linux ?**
```bash
chmod +x start.sh
```

**psutil ne s'installe pas ?**
Sur Ubuntu/Debian :
```bash
sudo apt-get install python3-dev
pip install psutil
```

## 📊 API Endpoints

- `GET /api/metrics` - Toutes les métriques
- `GET /api/cpu` - CPU uniquement
- `GET /api/memory` - Mémoire uniquement
- `GET /api/load` - Load average uniquement

Exemple :
```bash
curl http://localhost:5000/api/metrics | jq
```

## 🌟 Prochain Étapes

1. Consultez `CUSTOMIZATION.md` pour la personnalisation avancée
2. Regardez `templates/custom_example.html` pour des exemples
3. Ajoutez vos propres métriques personnalisées

---

**Besoin d'aide ?** Consultez la documentation complète dans `README.md`
