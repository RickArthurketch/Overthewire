import socket
import json
import time
import random

# À modifier avec l'adresse IP de ton Quest 3
IP_QUEST = "192.168.1.100" 
PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Envoi des données aléatoires vers {IP_QUEST}:{PORT}...")

try:
    while True:
        # Génère une respiration aléatoire entre 12.0 et 25.0
        respiration_aleatoire = round(random.uniform(12.0, 25.0), 1)
        
        # Crée le paquet JSON
        payload = {"rr": respiration_aleatoire}
        message = json.dumps(payload).encode("utf-8")
        
        # Envoie le paquet
        sock.sendto(message, (IP_QUEST, PORT))
        print(f"Envoyé : {payload}")
        
        # Pause d'une demi-seconde
        time.sleep(0.5) 
        
except KeyboardInterrupt:
    print("\nArrêt du programme.")
    sock.close()
