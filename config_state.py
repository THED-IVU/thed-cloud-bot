# 📄 config_state.py — Configuration dynamique pour le bot TIB

import streamlit as st
from ai import fournisseurs_ia, parser_resultat_ia
from runtime_config import get_runtime_config

# ------------------------------
# CONFIGURATION PAR DÉFAUT
# ------------------------------
BASE_CONFIG = {
    "symbol": "EURUSD",        # 📈 Actif par défaut
    "interval": 60,            # ⏱ Intervalle (en secondes)
    "use_ai": True,            # 🤖 Activer IA par défaut
    "capital": 1000,           # 💰 Capital de base
    "ai_provider": "openai",   # 🌐 Fournisseur IA par défaut
    # Ajouter d'autres clés si besoin
}

# ------------------------------
# UTILS - Fournisseurs IA actifs
# ------------------------------
def get_available_providers(config_dict):
    """Retourne la liste des fournisseurs IA valides (avec une clé API définie)."""
    return [
        key for key, value in config_dict.items()
        if isinstance(value, dict) and value.get("api_key")
    ]

# ------------------------------
# INTERFACE SIDEBAR STREAMLIT
# ------------------------------
def sidebar_config():
    st.sidebar.title("⚙️ Paramètres généraux du Bot TIB")

    # ✅ Configuration utilisateur standard
    st.session_state["symbol"] = st.sidebar.text_input(
        "📈 Symbole de trading", value=BASE_CONFIG.get("symbol", "EURUSD")
    )
    st.session_state["interval"] = st.sidebar.slider(
        "⏱ Intervalle (secondes)", 10, 300, value=BASE_CONFIG.get("interval", 60)
    )
    st.session_state["capital"] = st.sidebar.number_input(
        "💰 Capital de départ", min_value=10, value=BASE_CONFIG.get("capital", 1000)
    )

    # ✅ Activer/Désactiver l'IA
    use_ai = st.sidebar.checkbox(
        "🤖 Activer l'IA",
        value=st.session_state.get("use_ai", BASE_CONFIG.get("use_ai", True)),
        key="checkbox_use_ai"
    )
    st.session_state["use_ai"] = use_ai

    # ✅ Choix du fournisseur IA
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🧠 Fournisseur IA")

    providers_disponibles = get_available_providers(BASE_CONFIG)
    default_provider = BASE_CONFIG.get("ai_provider", "openai")
    default_index = providers_disponibles.index(default_provider) if default_provider in providers_disponibles else 0

    provider = st.sidebar.selectbox(
        "🌐 Sélectionner un fournisseur :",
        providers_disponibles,
        index=default_index,
        key="select_ai_provider"
    )
    st.session_state["ai_provider"] = provider

    # ✅ Test automatique IA (1ère fois)
    if "ia_autotest_done" not in st.session_state:
        st.session_state["ia_autotest_done"] = True

        if use_ai:
            with st.spinner("🔍 Test automatique de l'IA en cours..."):
                try:
                    runtime_config = get_runtime_config()
                    prompt_test = "Donne un conseil de trading rapide en une ligne."
                    ia_func = fournisseurs_ia.get(provider)

                    if ia_func:
                        result = ia_func(prompt_test, runtime_config)
                        parsed = parser_resultat_ia(result)

                        st.sidebar.markdown("🧠 **Réponse IA :**")
                        st.sidebar.code(result[:300])
                        st.sidebar.markdown("📊 **Résumé :**")
                        for k, v in parsed.items():
                            if v:
                                st.sidebar.markdown(f"**{k.capitalize()}**: {v}")
                        st.sidebar.success("🟢 IA fonctionnelle")
                    else:
                        st.sidebar.error("❌ Fonction IA introuvable.")
                except Exception as e:
                    st.sidebar.error("🔴 Erreur pendant le test IA")
                    st.sidebar.code(str(e))

    # ✅ Résumé actif
    st.sidebar.markdown("---")
    if use_ai:
        st.sidebar.success(f"✅ Mode IA activé avec {provider.upper()}")
    else:
        st.sidebar.warning("⚙️ Mode TECHNIQUE uniquement (sans IA)")

    model_name = BASE_CONFIG.get(provider, {}).get("model", "modèle inconnu")
    st.sidebar.info(f"🧬 Modèle : `{model_name}`")

    # ✅ Test IA manuel
    st.sidebar.markdown("## 🔬 Tester l’IA")

    if st.sidebar.button("🧪 Tester maintenant", key="btn_test_ia"):
        try:
            runtime_config = get_runtime_config()
            prompt_test = "Explique en une phrase la tendance probable du marché EURUSD."
            ia_func = fournisseurs_ia.get(provider)

            if ia_func:
                result = ia_func(prompt_test, runtime_config)
                parsed = parser_resultat_ia(result)

                st.sidebar.markdown("🧠 **Réponse brute :**")
                st.sidebar.code(result[:500])
                st.sidebar.markdown("📈 **Analyse IA :**")
                for k, v in parsed.items():
                    if v:
                        st.sidebar.markdown(f"**{k.capitalize()}**: {v}")
                st.sidebar.success("✅ L’IA a répondu.")
            else:
                st.sidebar.error("Fournisseur IA indisponible.")
        except Exception as e:
            st.sidebar.error("⚠️ Erreur lors de la requête IA")
            st.sidebar.code(str(e))

    # ✅ Forcer retest
    if st.sidebar.button("🔁 Relancer test IA", key="btn_retest_ia"):
        del st.session_state["ia_autotest_done"]
        st.experimental_rerun()

# ------------------------------
# CONFIGURATION RUNTIME DYNAMIQUE
# ------------------------------
def get_runtime_config():
    return {
        "symbol": st.session_state.get("symbol", BASE_CONFIG["symbol"]),
        "interval": st.session_state.get("interval", BASE_CONFIG["interval"]),
        "use_ai": st.session_state.get("use_ai", BASE_CONFIG["use_ai"]),
        "capital": st.session_state.get("capital", BASE_CONFIG["capital"]),
        "ai_provider": st.session_state.get("ai_provider", BASE_CONFIG.get("ai_provider", "openai")),
    }
