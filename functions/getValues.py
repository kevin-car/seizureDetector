# Import des fonctions
from functionsSecondary.announceVocal import announceVocal
from functionsSecondary.exportHeartValuesToBDD import export_heart_rate_to_influxdb
import asyncio
import time
from bleak import BleakClient, BleakScanner, BleakError
from pushover import Client

# Adresse MAC et UUID du capteur
ADDRESS = "DB:67:08:4A:61:7B"
HEART_RATE_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Variables pour surveiller les données de fréquence cardiaque
last_heart_rate = None
last_update_time = time.time()
HEART_RATE_TIMEOUT = 10  # Délai en secondes avant de considérer le capteur comme inactif

# Initialisation du client Pushover
pushover_client = Client("uvc9zcenk1h8j9xerj3149y3r4d6zk", api_token="asqvw3iis265xioiehgf2udv9zhcwv")

alert_sent = False  # Variable pour éviter les alertes répétées


def heart_rate_notification_handler(sender, data, ip_address):
    global last_heart_rate, last_update_time, alert_sent

    try:
        # Extraction de la fréquence cardiaque depuis `data`
        heart_rate = data[1]  # Assurez-vous que l'index est correct pour votre appareil
        current_time = time.time()

        # Gestion des cas où la fréquence cardiaque est 0
        if heart_rate == 0:
            print("Fréquence cardiaque = 0, lecture du son d'alerte...")
            asyncio.create_task(announceVocal("sonde mal mise"))
        else:
            # Mettre à jour les valeurs de référence si la fréquence cardiaque change
            last_heart_rate = heart_rate
            last_update_time = current_time
            print(f"Fréquence cardiaque: {heart_rate} bpm")
            export_heart_rate_to_influxdb(heart_rate, ADDRESS, ip_address)

            # Annonce de la fréquence cardiaque si elle est supérieure à un seuil
            print('Heart Rate:', heart_rate)
            if heart_rate > 80:
                asyncio.create_task(announceVocal(f"{heart_rate}"))

            if heart_rate > 80 and not alert_sent:
                pushover_client.send_message(
                    (f"Alerte ! Le coeur est à {heart_rate}"),
                    title="Alerte Importante",
                    priority=2,  # Priorité urgente
                    retry=30,  # Intervalle de répétition (en secondes)
                    expire=3600,  # Expiration de l'alerte après 1 heure
                    sound="persistent"  # Son persistant si disponible
                )
                alert_sent = True  # Marquer l'alerte comme envoyée

    except Exception as e:
        print(f"Erreur dans le gestionnaire de notifications : {e}")


async def connect_and_monitor_heart_rate(ip_address):
    while True:
        try:
            print("Recherche de l'appareil...")
            device = await BleakScanner.find_device_by_address(ADDRESS, timeout=10.0)

            if device:
                print(f"Appareil trouvé. Tentative de connexion à {ADDRESS}")
                async with BleakClient(device, timeout=5.0) as client:
                    print(f"Connecté à l'appareil : {ADDRESS}")
                    asyncio.create_task(announceVocal("connecté"))

                    # Début des notifications
                    await client.start_notify(
                        HEART_RATE_CHARACTERISTIC_UUID,
                        lambda sender, data: heart_rate_notification_handler(sender, data, ip_address)
                    )

                    # Maintien de la connexion
                    while client.is_connected:
                        await asyncio.sleep(1)

                    print("Déconnecté. Reconnexion en cours...")
                    asyncio.create_task(announceVocal("déconnecté"))
            else:
                print("Appareil non détecté. Nouvelle tentative dans 5 secondes.")
                asyncio.create_task(announceVocal("Appareil non détecté"))
                await asyncio.sleep(5)

        except asyncio.CancelledError:
            print("Processus annulé.")
            raise
        except TimeoutError:
            print("La connexion a expiré. Nouvelle tentative dans 5 secondes.")
            asyncio.create_task(announceVocal("connexion expirée"))
            await asyncio.sleep(5)
        except BleakError as e:
            print(f"Erreur de connexion : {e}. Nouvelle tentative dans 5 secondes.")
            asyncio.create_task(announceVocal("connexion perdue"))
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Erreur inattendue : {e}. Nouvelle tentative dans 5 secondes.")
            await asyncio.sleep(5)


async def start_heart_rate_monitoring(ip_address):
    await connect_and_monitor_heart_rate(ip_address)
