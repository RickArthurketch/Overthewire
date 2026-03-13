import asyncio
import json
import random
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions
)

# Utilise les mêmes UUIDs que dans ton script Java
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID    = "12345678-1234-5678-1234-56789abcdef1"

async def run(server):
    await server.start()
    print("Serveur BLE démarré. En attente du Quest 3...")

    while True:
        # Simulation de ton radar (à remplacer par la vraie lecture)
        respiration_val = random.uniform(5.0, 40.0) 
        
        # Création du JSON
        data = {"respiration": round(respiration_val, 1)}
        json_str = json.dumps(data)
        
        # Mise à jour de la donnée sur le Bluetooth
        server.get_characteristic(CHAR_UUID).value = json_str.encode('utf-8')
        
        # Pause de 50ms (envoie 20 fois par seconde)
        await asyncio.sleep(0.05) 

# Configuration du serveur
loop = asyncio.get_event_loop()
server = BlessServer(name="RaspPi_Radar", loop=loop)

# Ajout du service et de la caractéristique
server.add_new_service(SERVICE_UUID)
server.add_new_characteristic(
    SERVICE_UUID,
    CHAR_UUID,
    (GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify),
    json.dumps({"respiration": 0}).encode('utf-8'),
    (GATTAttributePermissions.readable | GATTAttributePermissions.writeable)
)

# Lancement
loop.run_until_complete(run(server))