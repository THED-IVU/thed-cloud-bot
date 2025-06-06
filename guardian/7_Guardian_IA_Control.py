import streamlit as st
from guardian.guardian_scanner import scanner_complet

st.set_page_config(page_title="🛡️ Panneau de Contrôle Guardian", layout="wide")
st.title("🛡️ Panneau de Contrôle du TIB Guardian")

# 📌 Section Scanner Complet
st.markdown("### 🔍 Scanner complet des fichiers (anomalies, TODO, erreurs...)")

if st.button("🚀 Lancer le scanner maintenant"):
    with st.spinner("Analyse en cours..."):
        rapport = scanner_complet(racine=".")
    st.session_state["dernier_rapport_scan"] = rapport
    st.success("✅ Scan terminé avec succès.")

# 📥 Affichage avec filtre
rapport = st.session_state.get("dernier_rapport_scan", None)
if rapport:
    st.markdown("### 🗂️ Résultat du dernier scan :")

    # 🎛️ Filtres
    options = ["Tous", "OK", "Vide", "À corriger", "Erreur"]
    choix = st.selectbox("🧰 Filtrer par statut :", options)

    for item in rapport:
        status = item["status"].lower()
        chemin = item["fichier"]
        afficher = False

        if choix == "Tous":
            afficher = True
        elif choix == "OK" and status == "ok":
            afficher = True
        elif choix == "Vide" and "vide" in status:
            afficher = True
        elif choix == "À corriger" and "à corriger" in status:
            afficher = True
        elif choix == "Erreur" and "erreur" in status:
            afficher = True

        if afficher:
            if status == "ok":
                st.markdown(f"✅ `{chemin}` – *OK*")
            elif "vide" in status:
                st.warning(f"🟡 `{chemin}` – *Fichier vide*")
            elif "à corriger" in status:
                st.error(f"🛠️ `{chemin}` – *À corriger : TODO/FIXME*")
            elif "erreur" in status:
                st.error(f"❌ `{chemin}` – *Erreur : {status}*")
