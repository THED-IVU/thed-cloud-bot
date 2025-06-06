# pocket_executor.py – Exécution binaire Pocket Option (popup visuelle + son + simulation/réel)

import time
import os
import random
import tkinter as tk
from playsound import playsound

# === CONFIGURATION ===
SIMULATION_MODE = True  # 🔁 Passe à False pour exécution réelle Selenium
ALERTE_SON = True       # 🔔 Joue un son à chaque exécution
ALERTE_POPUP = True     # 🪟 Affiche une popup visuelle

# === FONCTION PRINCIPALE ===
def executer_trade_binaires(signal: dict) -> str:
    direction = signal.get("direction", "haut").lower()
    montant = signal.get("mise", 1)
    duree = signal.get("duree", 60)

    print(f"📋 Traitement du trade : {direction.upper()}, ${montant}, durée {duree}s")

    if ALERTE_POPUP:
        afficher_popup(direction, montant, duree)
    if ALERTE_SON:
        jouer_son_alerte(direction)

    if SIMULATION_MODE:
        print("🧪 Mode simulation activé : Aucun clic réel.")
        enregistrer_simulation(direction, montant, duree)
        alerter_guardian(f"📡 SIMULATION TRADE: {direction.upper()} ${montant} pour {duree}s")
        return f"[SIMU] {direction.upper()} de ${montant} / {duree}s"

    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-data-dir=" + os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--profile-directory=Default")

        driver = webdriver.Chrome(options=options)
        driver.get("https://pocketoption.com/en/trading/")
        time.sleep(random.uniform(4, 6))

        montant_input = driver.find_element(By.CLASS_NAME, "amount-input__input")
        montant_input.clear()
        montant_input.send_keys(str(montant))
        time.sleep(1)

        if direction in ["haut", "up"]:
            bouton = driver.find_element(By.CLASS_NAME, "buy-green")
        else:
            bouton = driver.find_element(By.CLASS_NAME, "buy-red")
        bouton.click()
        time.sleep(random.uniform(2, 3))

        print("✅ Trade exécuté avec succès.")
        driver.quit()
        return f"[OK] {direction.upper()} ${montant} exécuté"

    except Exception as e:
        print(f"❌ Erreur : {e}")
        alerter_guardian(f"❌ ECHEC TRADE: {e}")
        return f"[ERREUR] {e}"

# === POPUP VISUELLE ===
def afficher_popup(direction, montant, duree):
    fenetre = tk.Tk()
    fenetre.title("CONFIRMATION TRADE")
    fenetre.geometry("400x150")
    fenetre.configure(bg="#222222")
    texte = f"TRADE : {direction.upper()} - {montant}$ / {duree}s"
    tk.Label(fenetre, text=texte, font=("Arial", 16), fg="white", bg="#222222").pack(pady=20)
    tk.Button(fenetre, text="OK", command=fenetre.destroy, bg="#00cc66", fg="white").pack()
    fenetre.attributes("-topmost", True)
    fenetre.after(5000, fenetre.destroy)
    fenetre.mainloop()

# === ALERTE SONORE PAR DIRECTION ===
def jouer_son_alerte(direction="up"):
    try:
        chemin_audio = f"assets/audio/alerte_{direction.lower()}.mp3"
        if os.path.exists(chemin_audio):
            playsound(chemin_audio)
        else:
            print(f"⚠️ Son manquant : {chemin_audio}")
    except Exception as e:
        print(f"⚠️ Erreur audio : {e}")

# === LOGGER EN SIMULATION ===
def enregistrer_simulation(direction, montant, duree):
    chemin = "logs/logs_simulations.txt"
    os.makedirs("logs", exist_ok=True)
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} | {direction.upper()} | ${montant} | {duree}s\n")

# === NOTIFICATION GUARDIAN IA ===
def alerter_guardian(message):
    try:
        from core.alert_bot import envoyer_alerte
        envoyer_alerte(message)
    except Exception as e:
        print(f"⚠️ Erreur alerte Guardian : {e}")
