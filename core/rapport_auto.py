from fpdf import FPDF
import pandas as pd
import yfinance as yf
from core.predictor_ia import predire_direction
from datetime import datetime
import os
from core.drive_uploader import upload_to_drive
from core.email_sender import send_email_with_attachment

class RapportIA(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "🧠 Rapport IA Hebdomadaire - THED BOT", 0, 1, "C")

    def chapitre(self, titre):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, titre, 0, 1, "L")
        self.ln(2)

    def ajout_tableau_ia_patterns(self, actifs, periode="7d", intervalle="1d"):
        self.set_font("Arial", "", 10)
        self.data_saved = []  # for historical usage
        for actif in actifs:
            df = yf.download(actif, period=periode, interval=intervalle)
            if df.empty:
                continue

            last_row = df.iloc[-1]
            data_tech = {
                "rsi": 55,
                "macd": 1.1,
                "ema9": df["Close"].ewm(span=9).mean().iloc[-1],
                "ema21": df["Close"].ewm(span=21).mean().iloc[-1],
                "bollinger_position": (last_row["Close"] - df["Close"].rolling(20).mean().iloc[-1]) / df["Close"].rolling(20).std().iloc[-1],
                "psar_trend": "up" if last_row["Close"] > df["Close"].ewm(span=21).mean().iloc[-1] else "down",
                "stoch_k": 45
            }
            res = predire_direction(actif, data_tech, df, "EMA+RSI+Patterns")
            self.data_saved.append({
                "Actif": actif,
                "Prédiction": res["prediction"],
                "Score": res["confiance"],
                "Bonus Pattern": res["details"]["bonus_pattern"]
            })

        self.set_fill_color(220, 220, 220)
        self.cell(45, 8, "Actif", 1, 0, "C", 1)
        self.cell(40, 8, "Prédiction", 1, 0, "C", 1)
        self.cell(30, 8, "Score IA", 1, 0, "C", 1)
        self.cell(45, 8, "Bonus Pattern", 1, 1, "C", 1)

        for row in self.data_saved:
            self.cell(45, 8, row["Actif"], 1)
            self.cell(40, 8, row["Prédiction"], 1)
            self.cell(30, 8, str(row["Score"]), 1)
            self.cell(45, 8, str(row["Bonus Pattern"]), 1)
            self.ln()

def sauvegarder_rapport_ia_pdf(version="semaine"):
    pdf = RapportIA()
    pdf.add_page()
    pdf.chapitre("📊 Résultats IA + Influence Patterns")
    actifs = ["BTC-USD", "EURUSD=X", "ETH-USD", "XAUUSD=X"]
    pdf.ajout_tableau_ia_patterns(actifs)
    nom = f"rapport_ia_{version}_{datetime.now().strftime('%Y%m%d')}.pdf"
    chemin = f"exports/{nom}"
    pdf.output(chemin)

    # Export vers Google Drive
    upload_to_drive(chemin)

    # Envoi Email
    send_email_with_attachment("thedhermann6@gmail.com", chemin)

    print(f"✅ Rapport IA exporté (PDF + Drive + Email) : {chemin}")