from flask import Flask, render_template, request, jsonify, send_file
import ffmpeg
import os
import json
import uuid
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max

# Créer les dossiers nécessaires
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Obtenir les informations de la vidéo
        probe = ffmpeg.probe(filepath)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'width': int(video_info['width']),
            'height': int(video_info['height']),
            'duration': float(probe['format']['duration']),
            'codec': video_info['codec_name']
        })
    
    return jsonify({'error': 'Type de fichier non autorisé'}), 400

@app.route('/process', methods=['POST'])
def process_video():
    try:
        data = request.json
        input_file = data.get('input_file')
        workflow = data.get('workflow')
        
        if not input_file or not workflow:
            return jsonify({'error': 'Paramètres manquants'}), 400
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file)
        if not os.path.exists(input_path):
            return jsonify({'error': 'Fichier source introuvable'}), 404
        
        # Créer le nom du fichier de sortie
        output_filename = f"output_{uuid.uuid4()}.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Construire le pipeline ffmpeg à partir du workflow
        stream = ffmpeg.input(input_path)
        
        # Traiter les nœuds dans l'ordre
        nodes = workflow.get('drawflow', {}).get('Home', {}).get('data', {})
        
        # Trier les nœuds par ordre de connexion
        sorted_nodes = sort_nodes_by_connection(nodes)
        
        # Appliquer les filtres dans l'ordre
        for node_id in sorted_nodes:
            node = nodes[node_id]
            node_name = node.get('name')
            node_data = node.get('data', {})
            
            if node_name == 'input':
                continue  # Déjà traité
            elif node_name == 'output':
                continue  # Traité à la fin
            else:
                # Appliquer le filtre
                stream = apply_filter(stream, node_name, node_data)
        
        # Sortie
        stream = ffmpeg.output(stream, output_path, 
                               vcodec='libx264',
                               acodec='aac',
                               strict='experimental')
        
        # Exécuter
        ffmpeg.run(stream, overwrite_output=True)
        
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'download_url': f'/download/{output_filename}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def sort_nodes_by_connection(nodes):
    """Trie les nœuds dans l'ordre de connexion"""
    sorted_ids = []
    connections = {}
    
    # Créer un mapping des connexions
    for node_id, node in nodes.items():
        outputs = node.get('outputs', {})
        for output_key, output_data in outputs.items():
            for conn in output_data.get('connections', []):
                target_node = str(conn.get('node'))
                if target_node not in connections:
                    connections[target_node] = []
                connections[target_node].append(node_id)
    
    # Commencer par le nœud input
    for node_id, node in nodes.items():
        if node.get('name') == 'input':
            sorted_ids.append(node_id)
            break
    
    # Parcourir les connexions
    visited = set(sorted_ids)
    queue = sorted_ids.copy()
    
    while queue:
        current = queue.pop(0)
        node = nodes.get(current)
        if not node:
            continue
            
        outputs = node.get('outputs', {})
        for output_key, output_data in outputs.items():
            for conn in output_data.get('connections', []):
                target_node = str(conn.get('node'))
                if target_node not in visited:
                    visited.add(target_node)
                    sorted_ids.append(target_node)
                    queue.append(target_node)
    
    return sorted_ids

def apply_filter(stream, filter_name, params):
    """Applique un filtre ffmpeg au stream"""
    try:
        if filter_name == 'scale':
            width = params.get('width', -1)
            height = params.get('height', -1)
            return stream.filter('scale', width, height)
        
        elif filter_name == 'crop':
            w = params.get('w', 'iw')
            h = params.get('h', 'ih')
            x = params.get('x', 0)
            y = params.get('y', 0)
            return stream.filter('crop', w, h, x, y)
        
        elif filter_name == 'rotate':
            angle = params.get('angle', 0)
            return stream.filter('rotate', f"{angle}*PI/180")
        
        elif filter_name == 'hflip':
            return stream.filter('hflip')
        
        elif filter_name == 'vflip':
            return stream.filter('vflip')
        
        elif filter_name == 'brightness':
            brightness = params.get('brightness', 0)
            return stream.filter('eq', brightness=brightness)
        
        elif filter_name == 'contrast':
            contrast = params.get('contrast', 1)
            return stream.filter('eq', contrast=contrast)
        
        elif filter_name == 'saturation':
            saturation = params.get('saturation', 1)
            return stream.filter('eq', saturation=saturation)
        
        elif filter_name == 'blur':
            sigma = params.get('sigma', 1)
            return stream.filter('gblur', sigma=sigma)
        
        elif filter_name == 'sharpen':
            amount = params.get('amount', 1.0)
            return stream.filter('unsharp', 5, 5, amount)
        
        elif filter_name == 'fade':
            fade_type = params.get('type', 'in')
            duration = params.get('duration', 1)
            return stream.filter('fade', type=fade_type, duration=duration)
        
        elif filter_name == 'grayscale':
            return stream.filter('hue', s=0)
        
        elif filter_name == 'speed':
            speed = params.get('speed', 1.0)
            return stream.filter('setpts', f'{1/speed}*PTS')
        
        elif filter_name == 'fps':
            fps = params.get('fps', 30)
            return stream.filter('fps', fps=fps)
        
        elif filter_name == 'trim':
            start = params.get('start', 0)
            end = params.get('end', None)
            if end:
                return stream.filter('trim', start=start, end=end).filter('setpts', 'PTS-STARTPTS')
            else:
                return stream.filter('trim', start=start).filter('setpts', 'PTS-STARTPTS')
        
        else:
            # Filtre générique
            return stream.filter(filter_name, **params)
            
    except Exception as e:
        print(f"Erreur lors de l'application du filtre {filter_name}: {e}")
        return stream

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['OUTPUT_FOLDER'], filename),
        as_attachment=True
    )

@app.route('/filters')
def get_filters():
    """Retourne la liste des filtres disponibles"""
    filters = [
        {
            'name': 'scale',
            'label': 'Redimensionner',
            'params': [
                {'name': 'width', 'label': 'Largeur', 'type': 'number', 'default': 1280},
                {'name': 'height', 'label': 'Hauteur', 'type': 'number', 'default': 720}
            ]
        },
        {
            'name': 'crop',
            'label': 'Rogner',
            'params': [
                {'name': 'w', 'label': 'Largeur', 'type': 'number', 'default': 640},
                {'name': 'h', 'label': 'Hauteur', 'type': 'number', 'default': 480},
                {'name': 'x', 'label': 'Position X', 'type': 'number', 'default': 0},
                {'name': 'y', 'label': 'Position Y', 'type': 'number', 'default': 0}
            ]
        },
        {
            'name': 'rotate',
            'label': 'Rotation',
            'params': [
                {'name': 'angle', 'label': 'Angle (degrés)', 'type': 'number', 'default': 0}
            ]
        },
        {
            'name': 'hflip',
            'label': 'Miroir horizontal',
            'params': []
        },
        {
            'name': 'vflip',
            'label': 'Miroir vertical',
            'params': []
        },
        {
            'name': 'brightness',
            'label': 'Luminosité',
            'params': [
                {'name': 'brightness', 'label': 'Luminosité', 'type': 'range', 'min': -1, 'max': 1, 'step': 0.1, 'default': 0}
            ]
        },
        {
            'name': 'contrast',
            'label': 'Contraste',
            'params': [
                {'name': 'contrast', 'label': 'Contraste', 'type': 'range', 'min': 0, 'max': 3, 'step': 0.1, 'default': 1}
            ]
        },
        {
            'name': 'saturation',
            'label': 'Saturation',
            'params': [
                {'name': 'saturation', 'label': 'Saturation', 'type': 'range', 'min': 0, 'max': 3, 'step': 0.1, 'default': 1}
            ]
        },
        {
            'name': 'blur',
            'label': 'Flou',
            'params': [
                {'name': 'sigma', 'label': 'Intensité', 'type': 'range', 'min': 0, 'max': 10, 'step': 0.5, 'default': 1}
            ]
        },
        {
            'name': 'sharpen',
            'label': 'Netteté',
            'params': [
                {'name': 'amount', 'label': 'Intensité', 'type': 'range', 'min': 0, 'max': 5, 'step': 0.1, 'default': 1}
            ]
        },
        {
            'name': 'fade',
            'label': 'Fondu',
            'params': [
                {'name': 'type', 'label': 'Type', 'type': 'select', 'options': ['in', 'out'], 'default': 'in'},
                {'name': 'duration', 'label': 'Durée (s)', 'type': 'number', 'default': 1}
            ]
        },
        {
            'name': 'grayscale',
            'label': 'Noir et blanc',
            'params': []
        },
        {
            'name': 'speed',
            'label': 'Vitesse',
            'params': [
                {'name': 'speed', 'label': 'Vitesse', 'type': 'range', 'min': 0.25, 'max': 4, 'step': 0.25, 'default': 1}
            ]
        },
        {
            'name': 'fps',
            'label': 'FPS',
            'params': [
                {'name': 'fps', 'label': 'Images par seconde', 'type': 'number', 'default': 30}
            ]
        },
        {
            'name': 'trim',
            'label': 'Découper',
            'params': [
                {'name': 'start', 'label': 'Début (s)', 'type': 'number', 'default': 0},
                {'name': 'end', 'label': 'Fin (s)', 'type': 'number', 'default': 10}
            ]
        }
    ]
    return jsonify(filters)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
