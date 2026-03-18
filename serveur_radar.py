import asyncio
import json
import random
from bless import (
    BlessServer,
    GATTCharacteristicProperties,
    GATTAttributePermissions
)

# Toujours nos identifiants de connexion
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID    = "12345678-1234-5678-1234-56789abcdef1"

async def run(loop):
    # On initialise le serveur ici
    server = BlessServer(name="Radar_Quest", loop=loop)

    # NOUVEAU : On ajoute les "await" qui manquaient pour créer les canaux
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
    print("Serveur BLE actif. En attente de la connexion du téléphone/Quest 3...")

    # Boucle d'envoi des données
    while True:
        respiration_val = random.uniform(5.0, 40.0) 
        data = {"respiration": round(respiration_val, 1)}
        json_str = json.dumps(data)
        
        server.get_characteristic(CHAR_UUID).value = json_str.encode('utf-8')
        print(f"Envoi BLE : {json_str}")
        
        await asyncio.sleep(0.05) 

# Lancement propre du script
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run(loop))
except KeyboardInterrupt:
    print("\nArrêt du serveur BLE.")