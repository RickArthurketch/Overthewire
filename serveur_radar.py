import asyncio
import json
import random
from bless import (
    BlessServer,
    GATTCharacteristicProperties,
    GATTAttributePermissions
)

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID    = "12345678-1234-5678-1234-56789abcdef1"

async def run(loop):
    # On initialise le serveur ici
    server = BlessServer(name="Radar_Quest", loop=loop)

    # L'ERREUR VENAIT D'ICI : Il manquait les "await" devant ces deux lignes
    await server.add_new_service(SERVICE_UUID)
    await server.add_new_characteristic(
        SERVICE_UUID,
        CHAR_UUID,
        (GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify),
        json.dumps({"respiration": 0}).encode('utf-8'),
        (GATTAttributePermissions.readable | GATTAttributePermissions.writeable)
    )

    # On démarre le serveur
    await server.start()
    print("Serveur BLE actif. En attente de la connexion du téléphone...")

    # Boucle d'envoi des données
    while True:
        respiration_val = random.uniform(5.0, 40.0) 
        data = {"respiration": round(respiration_val, 1)}
        json_str = json.dumps(data)
        
        # 1. Modifie la valeur locale de la caractéristique
        server.get_characteristic(CHAR_UUID).value = json_str.encode('utf-8')
        
        # 2. LA LIGNE MANQUANTE : Déclenche l'envoi de la notification au téléphone
        server.update_value(SERVICE_UUID, CHAR_UUID)
        
        print(f"Envoi BLE : {json_str}")
        
        # 3. Pause de 0.2 seconde pour stabiliser la connexion Android
        await asyncio.sleep(0.2) 

# Lancement propre du script
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run(loop))
except KeyboardInterrupt:
    print("\nArrêt du serveur BLE.")
