# 📦 db.py
# Centralisation des accès SQLite (lecture, écriture, requêtes agrégées)

import sqlite3
import pandas as pd
import os

DB_PATH = "historique_trades.db"
TABLE_NAME = "trades"

# ----------- Connexion Générique ----------- #
def get_connection(path=DB_PATH):
    return sqlite3.connect(path)

# ----------- Initialisation de table (auto-ajustée) ----------- #
def initialiser_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            datetime TEXT,
            action TEXT,
            price REAL,
            exit_price REAL,
            profit REAL,
            RSI REAL,
            MACD REAL,
            MACDs REAL,
            EMA9 REAL,
            EMA21 REAL,
            source TEXT,
            context TEXT,
            score REAL,
            score_ia TEXT,
            validation_ia TEXT,
            explication_ia TEXT,
            asset TEXT DEFAULT '',
            capital REAL
        )
    """)
    conn.commit()
    conn.close()

# Initialiser au chargement
try:
    initialiser_table()
except Exception as e:
    print(f"⚠️ Erreur lors de l'initialisation de la table : {e}")

# ----------- Écriture Générique ----------- #
def inserer_trade(trade: dict, table=TABLE_NAME):
    try:
        conn = get_connection()
        df = pd.DataFrame([trade])
        df.to_sql(table, conn, if_exists="append", index=False)
        conn.close()
    except Exception as e:
        print(f"❌ Erreur insertion SQLite : {e}")

# ----------- Lecture Complète ----------- #
def lire_trades(table=TABLE_NAME):
    try:
        conn = get_connection()
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Erreur lecture SQLite : {e}")
        return pd.DataFrame()

# ----------- Agrégats ----------- #
def stats_globales():
    df = lire_trades()
    if df.empty:
        return None
    return {
        "total_trades": len(df),
        "gain_total": df["profit"].sum(),
        "taux_reussite": (df["profit"] > 0).mean(),
        "gain_moyen": df["profit"].mean(),
        "derniers_trades": df.tail(10)
    }

# ----------- Filtres dynamiques ----------- #
def filtrer_trades(action=None, min_score=None, actif=None):
    df = lire_trades()
    if df.empty:
        return df

    if action:
        df = df[df["action"].str.upper() == action.upper()]
    if min_score:
        df = df[df["score"] >= min_score]
    if actif:
        df = df[df["asset"] == actif]

    return df.reset_index(drop=True)
