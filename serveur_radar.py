import asyncio
import json
import random
from bless import (
    BlessServer,
    GATTCharacteristicProperties,
    GATTAttributePermissions
)

# Ces UUIDs sont identiques à ceux de ton pont Java (BLEBridge.java)
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID    = "12345678-1234-5678-1234-56789abcdef1"

async def run(server):
    await server.start()
    print("Serveur BLE actif. En attente de la connexion du Quest 3...")

    while True:
        # Génération d'une valeur de respiration simulée (entre 5 et 40)
        respiration_val = random.uniform(5.0, 40.0) 
        
        # Création du JSON attendu par ton script C#
        data = {"respiration": round(respiration_val, 1)}
        json_str = json.dumps(data)
        
        # Mise à jour de la donnée sur le canal Bluetooth
        server.get_characteristic(CHAR_UUID).value = json_str.encode('utf-8')
        
        print(f"Envoi BLE : {json_str}")
        
        # Pause de 0.05 seconde (environ 20 envois par seconde)
        await asyncio.sleep(0.05) 

# Configuration du serveur BLE
loop = asyncio.get_event_loop()
server = BlessServer(name="Radar_Quest", loop=loop)

server.add_new_service(SERVICE_UUID)
server.add_new_characteristic(
    SERVICE_UUID,
    CHAR_UUID,
    (GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify),
    json.dumps({"respiration": 0}).encode('utf-8'),
    (GATTAttributePermissions.readable | GATTAttributePermissions.writeable)
)

# Lancement du script
try:
    loop.run_until_complete(run(server))
except KeyboardInterrupt:
    print("\nArrêt du serveur BLE.")