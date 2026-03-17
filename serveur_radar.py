import socket
import json
import time
import random

# Remplace par l'adresse IP exacte de ton casque Quest 3
IP_QUEST = "10.197.141.96" 
PORT = 5000

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Envoi UDP démarré vers {IP_QUEST}:{PORT}...")

try:
    while True:
        # Simulation de la donnée
        respiration_val = random.uniform(5.0, 40.0)
        data = {"respiration": round(respiration_val, 1)}
        json_str = json.dumps(data)

        # Envoi direct du paquet UDP
        sock.sendto(json_str.encode('utf-8'), (IP_QUEST, PORT))
        print(f"Envoyé : {json_str}")

        # Pause pour limiter à 20 envois par seconde
        time.sleep(0.05) 
except KeyboardInterrupt:
    print("\nArrêt du serveur UDP.")
    sock.close()