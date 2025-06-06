
# guardian/guardian_reporter.py

import json
from datetime import datetime
from pathlib import Path
from fpdf import FPDF  # pour `fpdf2`, c’est identique, mais beaucoup plus puissant et maintenu

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

def enregistrer_rapport_json(data, nom="rapport_guardian"):
    path = LOGS_DIR / f"{nom}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return str(path)

def enregistrer_rapport_pdf(data, nom="rapport_guardian"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("Rapport Guardian IA")
    pdf.set_author("Guardian Auto-Fix")
    pdf.cell(200, 10, txt="🛡️ Rapport de correction Guardian IA", ln=True, align="C")
    pdf.ln(10)

    for i, item in enumerate(data, 1):
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, f"{i}. Fichier : {item['fichier']}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 10, f"   - Type : {item['type']}", ln=True)
        if "fonctionnalite" in item:
            pdf.cell(0, 10, f"   - Fonctionnalité : {item['fonctionnalite']}", ln=True)
        if "correction" in item:
            pdf.multi_cell(0, 8, f"   - Correction : {item['correction']}")
        pdf.ln(2)

    output_path = LOGS_DIR / f"{nom}.pdf"
    pdf.output(str(output_path))
    return str(output_path)
