from gtts import gTTS
import pygame
import os
import asyncio

# Indicateur global pour suivre l'état de la lecture audio
is_playing = False

# Fonction asynchrone pour jouer l'audio sans bloquer
async def play_audio(file_path):
    global is_playing
    try:
        print(f"Tentative de lecture du fichier: {file_path}")
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Attendre la fin de la lecture sans bloquer le reste du programme
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Erreur lors de la lecture de l'audio: {e}")
    finally:
        is_playing = False  # Remettre l'indicateur à False une fois terminé

# Fonction asynchrone pour générer et lire l'annonce
async def announceVocal(message):
    global is_playing
    if is_playing:
        print("Une annonce est déjà en cours, nouvelle annonce ignorée.")
        return  # Ignore l'annonce si une autre est en cours

    is_playing = True  # Définir l'indicateur à True avant de commencer
    tts = gTTS(text=message, lang='fr')
    audio_file = "assets/message.mp3"
    tts.save(audio_file)
    
    # Exécution de la lecture audio en tâche de fond
    await play_audio(audio_file)
    
    os.remove(audio_file)
