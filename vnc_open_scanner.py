import pyVnc
import os
import subprocess
from PIL import Image

success_file = "success.txt"
failed_file = "failed.txt"

def read_ip_ports(filename):
    ip_ports = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(",")
            ip = parts[0]
            if len(parts) > 1:
                ports = parts[1].split("-")
            else:
                ports = ["5900"]
            ip_ports[ip] = ports
    return ip_ports


def connect_vnc(ip, port):
    try:
        client = pyVnc.Client(ip, port)
        fb = client.connect()
        return fb
    except pyVnc.AuthenticationError:
        print(f"Authentification requise pour se connecter à la VNC à {ip}:{port}")
        return False
    except Exception as e:
        print(f"Erreur lors de la connexion à la VNC à {ip}:{port} : {e}")
        return False


def create_virtual_display():
    # Créer un serveur X virtuel avec Xvfb
    xvfb_process = subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1280x720x24"])
    return xvfb_process


filename = input("Entrez le nom du fichier contenant les adresses IP et les ports: ")

ip_ports = read_ip_ports(filename)
connected_ips = {}
failed_ips = {}

# Créer un serveur X virtuel
xvfb_process = create_virtual_display()

# Utiliser le serveur X virtuel
os.environ["DISPLAY"] = ":99"

if not os.path.exists("screens"):
    os.makedirs("screens")

for ip, ports in ip_ports.items():
    for port in ports:
        connected = connect_vnc(ip, port)
        if connected:
            print(f"La connexion VNC à {ip}:{port} est réussie")
            if ip not in connected_ips:
                connected_ips[ip] = []
            connected_ips[ip].append(port)

            # Capture d'écran
            screen = Image.frombytes("RGB", (connected.width, connected.height), connected.framebuffer())
            screen.save(f"screens/{ip}_{port}.png")
            print(f"Capture d'écran de {ip}:{port} sauvegardée dans le dossier 'screens'")
        else:
            print(f"Impossible de se connecter à la VNC à {ip}:{port}")
            if ip not in failed_ips:
                failed_ips[ip] = []
            failed_ips[ip].append(port)

# Arrêter le serveur X virtuel
xvfb_process.terminate()

print("Connexions réussies :")
for ip, ports in connected_ips.items():
    print(f"{ip}:{ports}")
    with open(success_file, "w") as f:
        f.write("\n".join(f"{ip}:{ports}"))

print("Connexions échouées :")
for ip, ports in failed_ips.items():
    print(f"{ip}:{ports}")
    with open(failed_file, "w") as f:
        f.write("\n".join(f"{ip}:{ports}"))
