import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json().get('ip')
        return ip
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de l'adresse IP : {e}")
        return None