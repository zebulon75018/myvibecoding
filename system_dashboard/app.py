from flask import Flask, render_template, jsonify
import psutil
import platform
from datetime import datetime

app = Flask(__name__)

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
        'total': mem.total / (1024**3),  # GB
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
        'bytes_sent': net_io.bytes_sent / (1024**2),  # MB
        'bytes_recv': net_io.bytes_recv / (1024**2),
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }

def get_load_average():
    """Récupère le load average"""
    try:
        load = psutil.getloadavg()
        return {
            'load1': load[0],
            'load5': load[1],
            'load15': load[2]
        }
    except AttributeError:
        # Windows n'a pas getloadavg
        return {
            'load1': 0,
            'load5': 0,
            'load15': 0
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

@app.route('/')
def index():
    """Page principale du dashboard"""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    """API pour récupérer toutes les métriques"""
    return jsonify({
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'disk': get_disk_info(),
        'network': get_network_info(),
        'load': get_load_average(),
        'system': get_system_info(),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/cpu')
def get_cpu():
    """API pour récupérer uniquement les infos CPU"""
    return jsonify(get_cpu_info())

@app.route('/api/memory')
def get_memory():
    """API pour récupérer uniquement les infos mémoire"""
    return jsonify(get_memory_info())

@app.route('/api/load')
def get_load():
    """API pour récupérer uniquement le load average"""
    return jsonify(get_load_average())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
