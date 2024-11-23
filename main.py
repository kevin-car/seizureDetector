import os, time
import asyncio
import subprocess  # Pour exécuter des commandes systèmes comme espeak

from functionsSecondary.exportHeartValuesToBDD import export_heart_rate_to_influxdb
from functionsSecondary.publicIP import get_public_ip
from functions.discover import find_bluetooth_devices
from functions.getValues import start_heart_rate_monitoring

# Datas 
token = os.environ.get("INFLUXDB_TOKEN")
org = "kevin"
url = "http://192.168.1.245:8086"
bucket = "jonas"
db = "jonas2"
ADDRESS = "DB:67:08:4A:61:7B"
ip_address = get_public_ip()
print('ip_adress' + ip_address)

# Programme

choix1 = "Affichage des appareils Bluetooth"
choix2 = "Lire les valeurs"
choix3 = "TODO"

# Fonction pour l'annonce vocale d'une erreur
async def announceVocal(message):
    subprocess.run(["espeak", message])

# Affichage de tous les équipements Bluetooth
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
    loop = asyncio.get_event_loop()  # Créer la boucle d'événements ici
    while True:
        afficher_menu()
        choix = input("Sélectionnez une option: ")

        if choix == "1":
            loop.run_until_complete(searchBluetoothDevices())  # Attendre la complétion de la fonction asynchrone
        elif choix == "2":
            loop.run_until_complete(connectAndGetValues())  # Attendre la complétion de la fonction asynchrone
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