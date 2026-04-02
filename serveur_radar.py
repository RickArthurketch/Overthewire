import socket
import time
import random

# Remplace par l'adresse IP de ton casque Quest 3
IP_QUEST = "192.168.X.X" 
PORT = 5005

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Début de l'envoi des données vers {IP_QUEST}:{PORT}...")

try:
    while True:
        # Génère une valeur flottante aléatoire entre 12.0 et 25.0
        respiration = round(random.uniform(12.0, 25.0), 2)
        
        # Convertit le nombre en texte brut, comme attendu par ton script C#
        message = str(respiration).encode("utf-8")
        
        # Envoie le message via le réseau
        sock.sendto(message, (IP_QUEST, PORT))
        print(f"Donnée envoyée : {respiration} rpm")
        
        # Pause d'une seconde avant le prochain envoi
        time.sleep(1) 
        
except KeyboardInterrupt:
    print("\nArrêt de l'émetteur.")
    sock.close()
