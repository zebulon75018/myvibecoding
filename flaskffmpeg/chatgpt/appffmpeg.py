import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
import ffmpeg
import pprint

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max upload (ajuste si besoin)
app.config['JSON_SORT_KEYS'] = False  # on garde l'ordre lisible

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


###########################
# Helpers
###########################

def save_upload(file_storage):
    """
    Sauvegarde le fichier uploadé et renvoie le chemin.
    """
    ext = os.path.splitext(file_storage.filename)[1]
    video_id = str(uuid.uuid4()) + ext
    path = os.path.join(app.config['UPLOAD_FOLDER'], video_id)
    file_storage.save(path)
    return path, video_id


def build_ffmpeg_pipeline(graph_json, preview=False):
    """
    Transforme le graphe Drawflow (envoyé par le front) en pipeline ffmpeg-python.

    graph_json = {
      "nodes": {
        "1": { "name": "input", "data": {"path": "..."} , "outputs": {"out": [{"node":"2","input":"in"}]} },
        "2": { "name": "brightness", "data": {"brightness":0.2,"contrast":1.0}, ... },
        "3": { "name": "output", "data": {} }
      }
    }

    Idée:
    - on va parcourir les nodes dans l'ordre du flux: input -> filtres -> output
    - pour simplifier : on suppose une seule chaîne linéaire (pas de branchement/mixage audio compliqué)
    """

    nodes = graph_json.get("nodes", {})

    # Trouver le node "input"
    input_node_id = None
    for node_id, node in nodes.items():
        if node["name"] == "input":
            input_node_id = node_id
            break
    pprint.pprint(input_node_id) 

    if input_node_id is None:
        raise ValueError("Graph invalide: aucun node 'input' trouvé.")

    # On construit l'ordre de passage en suivant les connexions 'out'
    ordered_nodes = []
    current = input_node_id
    visited = set()

    while current and current not in visited:
        visited.add(current)
        ordered_nodes.append(current)

        outputs = nodes[current].get("outputs", {})
        next_id = None

        # Parcourt tous les ports (ex: "output_1", "out", etc.) et prend la 1ʳᵉ connexion dispo
        for port_key, connections in outputs.items():
            if isinstance(connections, list) and len(connections) > 0:
                next_id = connections[0].get("node")
                break

        current = next_id
        # outputs = nodes[current].get("outputs", {})
        # next_id = None
        #  if "out" in outputs and len(outputs["out"]) > 0:
            # On prend la première connexion
        #     next_id = outputs["out"][0]["node"]
        #  current = next_id
    pprint.pprint(current) 

    # Maintenant ordered_nodes est typiquement ["1","2","3"] → input, filtre, output
    # On va générer la chaîne ffmpeg-python vidéo uniquement (sans audio pour l'instant)

    stream = None
    input_path = None
    output_path = None

    for idx, node_id in enumerate(ordered_nodes):
        node = nodes[node_id]
        name = node["name"]
        data = node.get("data", {})

        if name == "input":
            # point d'entrée : ffmpeg.input
            input_path = data.get("path")
            if not input_path or not os.path.exists(input_path):
                raise ValueError("Chemin d'entrée invalide ou manquant.")
            stream = ffmpeg.input(input_path)

        elif name == "brightness":
            # exemple filtre brightness/contrast => eq
            # ffmpeg filter: eq=brightness=0.06:contrast=1.5:saturation=1.3 ...
            b = float(data.get("brightness", 0.0))
            c = float(data.get("contrast", 1.0))
            s = float(data.get("saturation", 1.0))
            stream = ffmpeg.filter(stream, 'eq',
                                   brightness=b,
                                   contrast=c,
                                   saturation=s)

        elif name == "crop":
            # crop: width, height, x, y
            w = data.get("w", 640)
            h = data.get("h", 360)
            x = data.get("x", 0)
            y = data.get("y", 0)
            stream = ffmpeg.crop(stream, x, y, w, h)

        elif name == "grayscale":
            # noir et blanc → format=gray
            stream = ffmpeg.filter(stream, 'format', 'gray')

        elif name == "scale":
            # resize
            width = data.get("width", 640)
            height = data.get("height", 360)
            stream = ffmpeg.filter(stream, 'scale', width, height)

        elif name == "output":
            # dernier noeud
            # si on est en mode preview, on ne rend qu'un court extrait
            out_name = f"{uuid.uuid4()}.mp4"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], out_name)

            # pour une preview on peut limiter à 3 secondes via .output(..., t=3)
            if preview:
                out_stream = ffmpeg.output(stream, output_path,
                                           vcodec='libx264',
                                           preset='veryfast',
                                           t=3,
                                           pix_fmt='yuv420p')
            else:
                out_stream = ffmpeg.output(stream, output_path,
                                           vcodec='libx264',
                                           preset='medium',
                                           pix_fmt='yuv420p')

            return out_stream, output_path

        else:
            # filtre inconnu
            raise ValueError(f"Node '{name}' non géré côté backend.")

    raise ValueError("Graph sans noeud 'output' valide.")


def run_ffmpeg_pipeline(graph_json, preview=False):
    """
    Build + run ffmpeg command, return output file path (string).
    """
    out_stream, out_path = build_ffmpeg_pipeline(graph_json, preview=preview)
    # Lance ffmpeg
    (
        out_stream
        .overwrite_output()
        .run(quiet=True)  # passe en True pour pas spammer logs serveur
    )
    return out_path


###########################
# Routes Flask
###########################

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_video():
    """
    Reçoit un fichier vidéo via <input type="file">.
    Retourne un id et le chemin relatif pour le front.
    """
    if 'video' not in request.files:
        return jsonify({"error": "Aucun fichier 'video' reçu"}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400

    path, vid_id = save_upload(file)
    return jsonify({
        "status": "ok",
        "video_id": vid_id,
        "path": path
    })


@app.route("/process", methods=["POST"])
def process_video():
    """
    Reçoit le graphe Drawflow en JSON.
    Lance ffmpeg-python pour rendre un extrait de preview.
    Retourne l'URL du rendu.
    """
    data = request.get_json()
    pprint.pprint(data)
    if data is None:
        return jsonify({"error": "JSON manquant"}), 400

    try:
        output_path = run_ffmpeg_pipeline(data, preview=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    filename = os.path.basename(output_path)
    return jsonify({
        "status": "ok",
        "output_file": filename,
        "url": f"/outputs/{filename}"
    })


@app.route("/render_full", methods=["POST"])
def render_full():
    """
    Comme /process mais sans preview (rend la vidéo complète).
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "JSON manquant"}), 400

    try:
        output_path = run_ffmpeg_pipeline(data, preview=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    filename = os.path.basename(output_path)
    return jsonify({
        "status": "ok",
        "output_file": filename,
        "url": f"/outputs/{filename}"
    })


@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=False)


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    # potentiellement utile si tu veux rejouer l'input côté <video>
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True)

