import asyncio
import json
import random
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions
)

# UUIDs correspondants au code Unity/Java
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID    = "12345678-1234-5678-1234-56789abcdef1"

async def run(server):
    await server.start()
    print("Serveur BLE prêt. En attente de la connexion du Quest 3...")

    while True:
        # Génère une valeur de respiration aléatoire pour le test
        respiration_val = random.uniform(5.0, 40.0) 
        
        # Formate la donnée en JSON
        data = {"respiration": round(respiration_val, 1)}
        json_str = json.dumps(data)
        
        # Met à jour la valeur sur le canal Bluetooth
        server.get_characteristic(CHAR_UUID).value = json_str.encode('utf-8')
        
        # Affiche ce qui est envoyé dans le terminal
        print(f"Donnée envoyée via Bluetooth : {json_str}")
        
        # Pause d'une seconde pour te laisser le temps d'observer la lumière dans le casque
        await asyncio.sleep(1.0) 

# Initialisation du serveur Bluetooth
loop = asyncio.get_event_loop()
server = BlessServer(name="RaspPi_Radar", loop=loop)

server.add_new_service(SERVICE_UUID)
server.add_new_characteristic(
    SERVICE_UUID,
    CHAR_UUID,
    (GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify),
    json.dumps({"respiration": 0}).encode('utf-8'),
    (GATTAttributePermissions.readable | GATTAttributePermissions.writeable)
)

# Lancement de la boucle
try:
    loop.run_until_complete(run(server))
except KeyboardInterrupt:
    print("\nArrêt du serveur.")