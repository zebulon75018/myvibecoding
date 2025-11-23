let editor;
let currentVideo = null;
let availableFilters = [];

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    initDrawflow();
    loadFilters();
    setupEventListeners();
});

// Initialiser Drawflow
function initDrawflow() {
    const container = document.getElementById('drawflow');
    editor = new Drawflow(container);
    
    editor.reroute = true;
    editor.reroute_fix_curvature = true;
    editor.force_first_input = false;
    
    editor.start();
    
    // Ajouter le nœud d'entrée par défaut
    addInputNode();
    
    // Ajouter le nœud de sortie par défaut
    addOutputNode();
}

// Charger les filtres disponibles depuis le backend
async function loadFilters() {
    try {
        const response = await fetch('/filters');
        availableFilters = await response.json();
        displayFilters();
    } catch (error) {
        console.error('Erreur lors du chargement des filtres:', error);
        showNotification('Erreur lors du chargement des filtres', 'error');
    }
}

// Afficher les filtres dans la sidebar
function displayFilters() {
    const filtersList = document.getElementById('filtersList');
    filtersList.innerHTML = '';
    
    availableFilters.forEach(filter => {
        const filterItem = document.createElement('div');
        filterItem.className = 'filter-item';
        filterItem.draggable = true;
        filterItem.dataset.filter = JSON.stringify(filter);
        
        const icon = getFilterIcon(filter.name);
        filterItem.innerHTML = `<i class="fas ${icon}"></i> ${filter.label}`;
        
        filterItem.addEventListener('dragstart', drag);
        filterItem.addEventListener('click', () => addFilterNode(filter));
        
        filtersList.appendChild(filterItem);
    });
}

// Obtenir l'icône pour un filtre
function getFilterIcon(filterName) {
    const icons = {
        'scale': 'fa-expand-arrows-alt',
        'crop': 'fa-crop',
        'rotate': 'fa-redo',
        'hflip': 'fa-arrows-alt-h',
        'vflip': 'fa-arrows-alt-v',
        'brightness': 'fa-sun',
        'contrast': 'fa-adjust',
        'saturation': 'fa-palette',
        'blur': 'fa-blur',
        'sharpen': 'fa-cut',
        'fade': 'fa-glass',
        'grayscale': 'fa-eye-slash',
        'speed': 'fa-tachometer-alt',
        'fps': 'fa-film',
        'trim': 'fa-scissors'
    };
    return icons[filterName] || 'fa-filter';
}

// Configuration des event listeners
function setupEventListeners() {
    // Upload de vidéo
    document.getElementById('videoUpload').addEventListener('change', handleVideoUpload);
    
    // Boutons
    document.getElementById('clearBtn').addEventListener('click', clearWorkflow);
    document.getElementById('processBtn').addEventListener('click', processVideo);
}

// Gestion de l'upload de vidéo
async function handleVideoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('video', file);
    
    showLoading(true);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentVideo = data;
            displayVideoInfo(data);
            showNotification('Vidéo chargée avec succès!', 'success');
        } else {
            showNotification(data.error || 'Erreur lors du chargement', 'error');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('Erreur lors du chargement de la vidéo', 'error');
    } finally {
        showLoading(false);
    }
}

// Afficher les informations de la vidéo
function displayVideoInfo(videoData) {
    const videoInfo = document.getElementById('videoInfo');
    videoInfo.innerHTML = `
        <p><strong>Fichier:</strong> ${videoData.filename}</p>
        <p><strong>Résolution:</strong> ${videoData.width}x${videoData.height}</p>
        <p><strong>Durée:</strong> ${videoData.duration.toFixed(2)}s</p>
        <p><strong>Codec:</strong> ${videoData.codec}</p>
    `;
}

// Ajouter le nœud d'entrée
function addInputNode() {
    const html = `
        <div class="title-box">
            <i class="fas fa-upload"></i> Entrée Vidéo
        </div>
        <div class="box">
            <p style="font-size: 0.85rem; color: #6b7280;">
                Source de la vidéo
            </p>
        </div>
    `;
    
    editor.addNode('input', 0, 1, 50, 100, 'node-input-video', {}, html);
}

// Ajouter le nœud de sortie
function addOutputNode() {
    const html = `
        <div class="title-box">
            <i class="fas fa-download"></i> Sortie Vidéo
        </div>
        <div class="box">
            <p style="font-size: 0.85rem; color: #6b7280;">
                Vidéo finale
            </p>
        </div>
    `;
    
    const posX = window.innerWidth - 400;
    editor.addNode('output', 1, 0, posX, 100, 'node-output-video', {}, html);
}

// Ajouter un nœud de filtre
function addFilterNode(filter) {
    const posX = Math.random() * (window.innerWidth - 600) + 300;
    const posY = Math.random() * 300 + 150;
    
    let html = `
        <div class="title-box">
            <i class="fas ${getFilterIcon(filter.name)}"></i> ${filter.label}
        </div>
        <div class="box">
    `;
    
    const params = {};
    
    filter.params.forEach(param => {
        params[param.name] = param.default;
        
        if (param.type === 'number') {
            html += `
                <div class="node-input">
                    <label>${param.label}</label>
                    <input type="number" 
                           name="${param.name}" 
                           value="${param.default}"
                           onchange="updateNodeData(this, ${editor.nodeId + 1})">
                </div>
            `;
        } else if (param.type === 'range') {
            html += `
                <div class="node-input">
                    <label>${param.label}</label>
                    <input type="range" 
                           name="${param.name}" 
                           min="${param.min}" 
                           max="${param.max}" 
                           step="${param.step}" 
                           value="${param.default}"
                           oninput="updateNodeData(this, ${editor.nodeId + 1}); 
                                    this.nextElementSibling.textContent = this.value">
                    <span class="range-value">${param.default}</span>
                </div>
            `;
        } else if (param.type === 'select') {
            html += `
                <div class="node-input">
                    <label>${param.label}</label>
                    <select name="${param.name}" 
                            onchange="updateNodeData(this, ${editor.nodeId + 1})">
            `;
            param.options.forEach(option => {
                const selected = option === param.default ? 'selected' : '';
                html += `<option value="${option}" ${selected}>${option}</option>`;
            });
            html += `
                    </select>
                </div>
            `;
        }
    });
    
    html += '</div>';
    
    editor.addNode(filter.name, 1, 1, posX, posY, 'drawflow-node', params, html);
}

// Mettre à jour les données d'un nœud
function updateNodeData(element, nodeId) {
    const nodeName = element.getAttribute('name');
    const nodeValue = element.type === 'number' ? 
        parseFloat(element.value) : 
        (element.type === 'range' ? parseFloat(element.value) : element.value);
    
    const nodeData = editor.getNodeFromId(nodeId);
    if (nodeData) {
        nodeData.data[nodeName] = nodeValue;
    }
}

// Drag & Drop
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData('filter', ev.target.dataset.filter);
}

function drop(ev) {
    ev.preventDefault();
    const filterData = ev.dataTransfer.getData('filter');
    if (filterData) {
        const filter = JSON.parse(filterData);
        addFilterNode(filter);
    }
}

// Effacer le workflow
function clearWorkflow() {
    if (confirm('Êtes-vous sûr de vouloir effacer tout le workflow ?')) {
        editor.clear();
        addInputNode();
        addOutputNode();
        showNotification('Workflow effacé', 'info');
    }
}

// Traiter la vidéo
async function processVideo() {
    if (!currentVideo) {
        showNotification('Veuillez d\'abord charger une vidéo', 'error');
        return;
    }
    
    const exportData = editor.export();
    
    // Vérifier qu'il y a au moins une connexion
    const nodes = exportData.drawflow.Home.data;
    let hasConnections = false;
    
    for (let nodeId in nodes) {
        const node = nodes[nodeId];
        if (node.outputs && Object.keys(node.outputs).length > 0) {
            for (let outputKey in node.outputs) {
                if (node.outputs[outputKey].connections.length > 0) {
                    hasConnections = true;
                    break;
                }
            }
        }
        if (hasConnections) break;
    }
    
    if (!hasConnections) {
        showNotification('Veuillez connecter au moins un filtre', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                input_file: currentVideo.filename,
                workflow: exportData
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult(data);
            showNotification('Vidéo traitée avec succès!', 'success');
        } else {
            showNotification(data.error || 'Erreur lors du traitement', 'error');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showNotification('Erreur lors du traitement de la vidéo', 'error');
    } finally {
        showLoading(false);
    }
}

// Afficher le résultat
function displayResult(data) {
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');
    
    resultContent.innerHTML = `
        <p>Vidéo traitée avec succès!</p>
        <a href="${data.download_url}" class="btn btn-primary" download>
            <i class="fas fa-download"></i> Télécharger la vidéo
        </a>
    `;
    
    resultSection.style.display = 'block';
}

// Afficher/masquer le loading
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
}

// Afficher une notification
function showNotification(message, type = 'info') {
    // Créer une notification simple
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#667eea'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Ajouter les animations CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
