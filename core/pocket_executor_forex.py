# pocket_executor_forex.py – Exécution FOREX Pocket Option avec TP/SL/levier + popup + son

import os
import time
import random
import tkinter as tk
from playsound import playsound

# === CONFIGURATION ===
SIMULATION_MODE = True
ALERTE_POPUP = True
ALERTE_SON = True

# === FONCTION PRINCIPALE ===
def executer_trade_forex(signal: dict) -> str:
    symbol = signal.get("symbol", "EURUSD")
    direction = signal.get("direction", "buy").lower()
    lot = signal.get("lot", 0.01)
    leverage = signal.get("leverage", 50)
    tp = signal.get("tp", None)  # Take Profit
    sl = signal.get("sl", None)  # Stop Loss

    print(f"📋 FOREX Trade: {direction.upper()} {symbol} | Lot: {lot} | Lev: {leverage} | TP: {tp} | SL: {sl}")

    if ALERTE_POPUP:
        afficher_popup_forex(symbol, direction, lot, leverage, tp, sl)
    if ALERTE_SON:
        jouer_son_alerte(direction)

    if SIMULATION_MODE:
        print("🧪 Simulation activée : aucun ordre réel.")
        enregistrer_simulation_forex(symbol, direction, lot, leverage, tp, sl)
        alerter_guardian(f"📡 SIMU FOREX: {direction.upper()} {symbol} @lot={lot}, lev={leverage}")
        return f"[SIMU] {direction.upper()} {symbol} @lot={lot}, lev={leverage}"

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
        time.sleep(5)

        # Exemple générique : À adapter selon le DOM réel Pocket Option Forex
        lot_input = driver.find_element(By.CLASS_NAME, "amount-input__input")
        lot_input.clear()
        lot_input.send_keys(str(lot))
        time.sleep(1)

        if direction in ["buy", "achat", "haut", "up"]:
            bouton = driver.find_element(By.CLASS_NAME, "buy-green")
        else:
            bouton = driver.find_element(By.CLASS_NAME, "buy-red")
        bouton.click()
        print("✅ Ordre FOREX exécuté")
        time.sleep(2)
        driver.quit()
        return f"[OK] {direction.upper()} {symbol} FOREX exécuté"

    except Exception as e:
        print(f"❌ Erreur exécution FOREX : {e}")
        alerter_guardian(f"❌ ECHEC FOREX: {e}")
        return f"[ERREUR] {e}"

# === POPUP VISUELLE FOREX ===
def afficher_popup_forex(symbol, direction, lot, leverage, tp, sl):
    fenetre = tk.Tk()
    fenetre.title("TRADE FOREX")
    fenetre.geometry("450x180")
    fenetre.configure(bg="#111")
    texte = f"{symbol} – {direction.upper()} | Lot: {lot} | Lev: {leverage}\nTP: {tp or 'N/A'} | SL: {sl or 'N/A'}"
    tk.Label(fenetre, text=texte, font=("Arial", 14), fg="white", bg="#111").pack(pady=20)
    tk.Button(fenetre, text="OK", command=fenetre.destroy, bg="#1f8b4c", fg="white").pack()
    fenetre.attributes("-topmost", True)
    fenetre.after(5000, fenetre.destroy)
    fenetre.mainloop()

# === SON ALERTES PAR DIRECTION ===
def jouer_son_alerte(direction="buy"):
    try:
        fichier = "up" if direction in ["buy", "up", "haut", "achat"] else "down"
        chemin_audio = f"assets/audio/alerte_{fichier}.mp3"
        if os.path.exists(chemin_audio):
            playsound(chemin_audio)
        else:
            print(f"⚠️ Son manquant : {chemin_audio}")
    except Exception as e:
        print(f"⚠️ Erreur audio : {e}")

# === LOGGER FOREX ===
def enregistrer_simulation_forex(symbol, direction, lot, leverage, tp, sl):
    chemin = "logs/logs_forex.txt"
    os.makedirs("logs", exist_ok=True)
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} | {symbol} | {direction.upper()} | lot={lot} | lev={leverage} | TP={tp} | SL={sl}\n")

# === ALERTES GUARDIAN ===
def alerter_guardian(message):
    try:
        from core.alert_bot import envoyer_alerte
        envoyer_alerte(message)
    except Exception as e:
        print(f"⚠️ Guardian indisponible : {e}")
