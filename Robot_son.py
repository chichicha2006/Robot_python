# -*- coding: utf-8 -*-

import pyttsx3

#pour pas afficher le texte de pygame en console
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import time
import threading
import socket
import getpass

engine = pyttsx3.init()
engine.setProperty("rate", 200)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

text_queue = []
#-----------------------------------------------------------------------
# je reprend bassem_son et j'ajoute des print apres parler() dans chaque fonction pour pouvoir tester


def recevoir_texte_unity(texte):
    """Ajoute le texte reçu depuis Unity dans la file."""
    if texte:
        text_queue.append(texte.lower().strip())


def ecouter():
    """Remplace l'écoute micro : récupère le prochain texte Unity."""
    if len(text_queue) == 0:
        return None

    texte = text_queue.pop(0)
    #print("Texte Unity utilisé par ecouter() :", texte)

    if mots_interdits(texte):
        return mots_interdits(texte)

    return texte


def parler(text):
    print("BASSEM :", text)
    engine.say(text)
    engine.runAndWait()

 
def allo():
    texte = ecouter()
    if "bassem" in texte:
        parler("Oué, c'est greg?")
        print("Oué, c'est greg?")

def musique(a):
    def play():
        pygame.mixer.init()
        pygame.mixer.music.load(a)
        pygame.mixer.music.play()
        print(f"Lecture de {a} en cours...")
    parler("Pas de soucis, écoute ça")
    print("Pas de soucis, écoute ça")
    threading.Thread(target=play).start()

def stop():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    else:
        print("Aucune musique en cours.")

def volume(val):
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(val)
        parler(f"Volume réglé à {int(val * 100)} %")
        print("Volume réglé à {int(val * 100)} %")
    else:
        print("La musique n'est pas encore lancée.")

def juke():
    parler("Veux-tu écouter de la musique ?")
    print("Veux-tu écouter de la musique ?")
    texte = ecouter()
    if texte and ("oui" in texte or "yes" in texte):
        parler("Quel genre souhaites-tu écouter ? J'ai du romantique, de la pop, du jazz fusion, du rock.")
        print("Quel genre souhaites-tu écouter ? J'ai du romantique, de la pop, du jazz fusion, du rock.")
        texte = ecouter()
        if "romantique" in texte:
            musique("son/rizz.mp3")
            time.sleep(6)
            #oeil.coeur()
        elif "pop" in texte:
            #oeil.base()
            musique("son/pop.mp3")
        elif "jazz fusion" in texte:
           # oeil.croix()
            musique("son/jazz_fusion.mp3")
        elif "rock" in texte:
            #oeil.base()
            musique("son/lotta.mp3")
        texte = ecouter()
        if "stop" in texte:
            stop()
            parler("Ok, j'arrête ")
            print("Ok, j'arrête ")
    else:
        parler("pas de musique alors")
        print("pas de musique alors")
        

def get_ip():
    try:
        # Crée une connexion fictive pour obtenir l’IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # on ne contacte pas vraiment Google
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return ""
        
def mots_interdits(a):
    vulgaire=["enculé", "enculer", "pute","connard","merde","test controle"]
    wesh = ["wesh", "wech"]
    for element in vulgaire:
        if a in element :
            
            avertissement = "❌ grossier personnage. j'ai ton adresse I P ("+get_ip()+"), le login de ton compte utilisateur ("+getpass.getuser()+") et la machine où tu te trouve ("+socket.gethostname()+") . J'envoie tes identifiants et le message que tu as essayé de me faire dire aux services concernés." 
            parler(avertissement)
            print(avertissement)
            return True
        elif a in wesh:
            parler("on ne dit pas wesh dans une salle de classe")
            print("on ne dit pas wesh dans une salle de classe")
            return True
    return False

def reagir_au_texte(texte):
    """
    Fonction appelée par server.py à chaque texte reçu depuis Unity.
    Elle garde la logique de bassem_son.
    """
    recevoir_texte_unity(texte)

    #texte_min = texte.lower().strip()

    if "allô bassem" in texte or "bassem" in texte:
        allo()

    elif "musique" in texte:
        juke()

    elif "stop" in texte or "arrête" in texte:
        stop()
        parler("Ok, j'arrête.")

    elif "pop" in texte:
        musique("son/pop.mp3")

    elif "rock" in texte:
        musique("son/lotta.mp3")

    elif "romantique" in texte:
        musique("son/rizz.mp3")

    elif "jazz" in texte:
        musique("son/jazz_fusion.mp3")
    elif "test controle" in texte:
        avertissement = "❌ grossier personnage. j'ai ton adresse I P ("+get_ip()+"), le login de ton compte utilisateur ("+getpass.getuser()+") et la machine où tu te trouve ("+socket.gethostname()+") . J'envoie tes identifiants et le message que tu as essayé de me faire dire aux services concernés." 
        print(avertissement)
    else:
        parler("Je n'ai pas compris.")













