"""
Exemple d'utilisation de l'API de l'éditeur vidéo
Ce script montre comment interagir avec l'API Flask directement
"""

import requests
import json

# URL de base de l'API
BASE_URL = "http://localhost:5000"

def upload_video(video_path):
    """Upload une vidéo et retourne ses informations"""
    with open(video_path, 'rb') as f:
        files = {'video': f}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        return response.json()

def get_filters():
    """Récupère la liste des filtres disponibles"""
    response = requests.get(f"{BASE_URL}/filters")
    return response.json()

def process_video(input_filename, workflow):
    """Traite une vidéo avec un workflow donné"""
    data = {
        'input_file': input_filename,
        'workflow': workflow
    }
    response = requests.post(
        f"{BASE_URL}/process",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()

def download_video(output_filename, save_path):
    """Télécharge une vidéo traitée"""
    response = requests.get(f"{BASE_URL}/download/{output_filename}", stream=True)
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Vidéo téléchargée: {save_path}")

# Exemple d'utilisation
if __name__ == "__main__":
    # 1. Upload une vidéo
    print("Upload de la vidéo...")
    video_info = upload_video("mon_video.mp4")
    print(f"Vidéo uploadée: {video_info}")
    
    # 2. Créer un workflow simple: Input -> Scale -> Brightness -> Output
    workflow = {
        "drawflow": {
            "Home": {
                "data": {
                    "1": {
                        "id": 1,
                        "name": "input",
                        "data": {},
                        "class": "node-input-video",
                        "html": "",
                        "typenode": False,
                        "inputs": {},
                        "outputs": {
                            "output_1": {
                                "connections": [
                                    {"node": "2", "output": "input_1"}
                                ]
                            }
                        },
                        "pos_x": 50,
                        "pos_y": 100
                    },
                    "2": {
                        "id": 2,
                        "name": "scale",
                        "data": {
                            "width": 1280,
                            "height": 720
                        },
                        "class": "drawflow-node",
                        "html": "",
                        "typenode": False,
                        "inputs": {
                            "input_1": {
                                "connections": [
                                    {"node": "1", "input": "output_1"}
                                ]
                            }
                        },
                        "outputs": {
                            "output_1": {
                                "connections": [
                                    {"node": "3", "output": "input_1"}
                                ]
                            }
                        },
                        "pos_x": 300,
                        "pos_y": 100
                    },
                    "3": {
                        "id": 3,
                        "name": "brightness",
                        "data": {
                            "brightness": 0.2
                        },
                        "class": "drawflow-node",
                        "html": "",
                        "typenode": False,
                        "inputs": {
                            "input_1": {
                                "connections": [
                                    {"node": "2", "input": "output_1"}
                                ]
                            }
                        },
                        "outputs": {
                            "output_1": {
                                "connections": [
                                    {"node": "4", "output": "input_1"}
                                ]
                            }
                        },
                        "pos_x": 550,
                        "pos_y": 100
                    },
                    "4": {
                        "id": 4,
                        "name": "output",
                        "data": {},
                        "class": "node-output-video",
                        "html": "",
                        "typenode": False,
                        "inputs": {
                            "input_1": {
                                "connections": [
                                    {"node": "3", "input": "output_1"}
                                ]
                            }
                        },
                        "outputs": {},
                        "pos_x": 800,
                        "pos_y": 100
                    }
                }
            }
        }
    }
    
    # 3. Traiter la vidéo
    print("Traitement de la vidéo...")
    result = process_video(video_info['filename'], workflow)
    print(f"Résultat: {result}")
    
    # 4. Télécharger le résultat
    if result.get('success'):
        print("Téléchargement de la vidéo traitée...")
        download_video(result['output_file'], "video_traitee.mp4")
        print("✅ Terminé!")
    else:
        print(f"❌ Erreur: {result.get('error')}")
