from influxdb_client import InfluxDBClient, Point, WriteOptions
from datetime import datetime
import pytz
import requests 

# Configuration InfluxDB
INFLUXDB_URL = "http://localhost:8086"  # Changez cela si nécessaire
INFLUXDB_TOKEN = "mIRcv63okluvQdD_CyMThk63LBW_nQ3SrTPpO5YvHtytKQQvGusFygnqDc_AscMrf3byt6EcUh3w11MqFbV4Lg=="
INFLUXDB_ORG = "kevin"  # Remplacez par votre organisation
INFLUXDB_BUCKET = "jonas"  # Remplacez par votre bucket

# Créez le client InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

def get_timezone_from_ip(ip_address):
    try:
        response = requests.get(f'http://ipinfo.io/{ip_address}/json')
        data = response.json()
        return data.get("timezone")
    except Exception as e:
        print(f"Erreur lors de la récupération du fuseau horaire : {e}")
        return None

def export_heart_rate_to_influxdb(heart_rate, device_address, ip_address):
    timezone = get_timezone_from_ip(ip_address)

    if timezone:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
    else:
        now = datetime.utcnow()  # Par défaut, UTC si le fuseau horaire est introuvable

    # Vérification du type de `heart_rate`
    if not isinstance(heart_rate, (int, float)):
        print("Erreur : la valeur de heart_rate doit être un nombre.")
        return

    # Création du point de données avec le champ `bpm` et un horodatage précis
    point = Point("heart_rate") \
        .field("bpm", heart_rate) \
        .time(now)
    
    try:
        # Tentative d'écriture dans InfluxDB
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"Donnée exportée : {heart_rate} bpm à {datetime.utcnow()}")
    except Exception as e:
        # Capture de l'exception sans interrompre l'exécution
        print(f"Erreur lors de l'écriture dans InfluxDB : {e}")
        print("Les données de fréquence cardiaque n'ont pas été exportées.")
    
    # Continuation de l'exécution après l'erreur (si elle se produit)
    print("Tentative d'export terminée, on continue.")
