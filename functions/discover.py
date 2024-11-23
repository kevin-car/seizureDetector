import asyncio
from bleak import BleakScanner

# afficher tous les équipements visible en bluetoth 
async def find_bluetooth_devices():
    print("Recherche des appareils Bluetooth...")
    devices = await BleakScanner.discover()
    
    print("Appareils trouvés:")
    for device in devices:
        print(f"{device.name} - {device.address} - RSSI: {device.rssi} dBm")