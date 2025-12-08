from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psutil
import platform
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Variable globale pour contrôler le thread de mise à jour
update_thread = None
thread_lock = threading.Lock()

def get_cpu_info():
    """Récupère les informations CPU"""
    return {
        'percent': psutil.cpu_percent(interval=1),
        'count': psutil.cpu_count(),
        'freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
        'per_cpu': psutil.cpu_percent(interval=1, percpu=True)
    }

def get_memory_info():
    """Récupère les informations mémoire"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        'total': mem.total / (1024**3),
        'available': mem.available / (1024**3),
        'used': mem.used / (1024**3),
        'percent': mem.percent,
        'swap_total': swap.total / (1024**3),
        'swap_used': swap.used / (1024**3),
        'swap_percent': swap.percent
    }

def get_disk_info():
    """Récupère les informations disque"""
    partitions = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total / (1024**3),
                'used': usage.used / (1024**3),
                'free': usage.free / (1024**3),
                'percent': usage.percent
            })
        except PermissionError:
            continue
    return partitions

def get_network_info():
    """Récupère les informations réseau"""
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': net_io.bytes_sent / (1024**2),
        'bytes_recv': net_io.bytes_recv / (1024**2),
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }

def get_load_average():
    """Récupère le load average (Linux uniquement)"""
    load = psutil.getloadavg()
    return {
        'load1': load[0],
        'load5': load[1],
        'load15': load[2]
    }

def get_system_info():
    """Récupère les informations système"""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'hostname': platform.node(),
        'processor': platform.processor(),
        'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        'uptime': str(uptime).split('.')[0]
    }

def get_all_metrics():
    """Récupère toutes les métriques système"""
    return {
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'disk': get_disk_info(),
        'network': get_network_info(),
        'load': get_load_average(),
        'system': get_system_info(),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def background_metrics_updater():
    """Thread en arrière-plan qui émet les métriques toutes les 2 secondes"""
    while True:
        try:
            metrics = get_all_metrics()
            socketio.emit('metrics_update', metrics, namespace='/')
            time.sleep(2)
        except Exception as e:
            print(f"Erreur dans le thread de mise à jour: {e}")
            time.sleep(2)

@app.route('/')
def index():
    """Page principale du dashboard"""
    return render_template('dashboard.html')

@socketio.on('connect')
def handle_connect():
    """Gestion de la connexion WebSocket"""
    print('Client connecté')
    global update_thread
    with thread_lock:
        if update_thread is None:
            update_thread = threading.Thread(target=background_metrics_updater)
            update_thread.daemon = True
            update_thread.start()
    
    # Envoyer immédiatement les métriques actuelles
    emit('metrics_update', get_all_metrics())

@socketio.on('disconnect')
def handle_disconnect():
    """Gestion de la déconnexion WebSocket"""
    print('Client déconnecté')

@socketio.on('request_metrics')
def handle_request_metrics():
    """Gestion de la demande manuelle de métriques"""
    emit('metrics_update', get_all_metrics())

if __name__ == '__main__':
    print("="*50)
    print("  Dashboard Système avec WebSockets")
    print("="*50)
    print(f"  URL: http://localhost:5000")
    print(f"  Plateforme: {platform.system()}")
    print("="*50)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
