import os
import asyncio
import subprocess  # Pour exécuter des commandes systèmes comme espeak

from functionsSecondary.exportHeartValuesToBDD import export_heart_rate_to_influxdb
from functionsSecondary.publicIP import get_public_ip
from functions.discover import find_bluetooth_devices
from functions.getValues import start_heart_rate_monitoring

ip_address = get_public_ip()
print('ip_adress' + ip_address)

# Programme
choix1 = "Affichage des appareils Bluetooth"
choix2 = "Démarrer le monitoring"
choix3 = "TODO"

async def announceVocal(message):
    subprocess.run(["espeak", message])

async def searchBluetoothDevices():
    try:
        print(choix1)
        await find_bluetooth_devices()
    except Exception as e:
        print(f"Erreur dans searchBluetoothDevices : {e}")
        asyncio.create_task(announceVocal("disconnected"))

# Lancement du monitoring
async def connectAndGetValues():
    try:
        print(choix2)
        await start_heart_rate_monitoring(ip_address)
    except Exception as e:
        print(f"Erreur dans connectAndGetValues : {e}")
        asyncio.create_task(announceVocal("disconnected"))

# future fonction
def option3():
    print('test')

def afficher_menu():
    print("\n--- Menu ---")
    print("1: Option 1 : " + choix1)
    print("2: Option 2 : " + choix2)
    print("3: Option 3")
    print("0: Quitter")

def menu():
    loop = asyncio.get_event_loop()
    while True:
        afficher_menu()
        choix = input("Sélectionnez une option: ")

        if choix == "1":
            loop.run_until_complete(searchBluetoothDevices()) 
        elif choix == "2":
            loop.run_until_complete(connectAndGetValues()) 
        elif choix == "3":
            option3()
        elif choix == "0":
            print("Au revoir!")
            break
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    try:
        menu()
    except Exception as e:
        print(f"Erreur générale dans le programme : {e}")
        asyncio.create_task(announceVocal("disconnected"))
