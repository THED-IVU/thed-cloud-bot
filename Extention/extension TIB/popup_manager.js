// 🧠 Gestion centralisée des popups IA + injection dynamique

window.THEDBOT_POPUP_CACHE = {};

window.PopupManager = {
  index: 0,
  spacing: 160, // Espace vertical entre les popups

  /**
   * Affiche un popup IA avec gestion automatique des doublons, positions et fermeture.
   */
  showPopup: function (contentHTML, id = null, autoClose = true, duration = 15000) {
    const popupId = id || `popup_${Date.now()}`;
    if (window.THEDBOT_POPUP_CACHE[popupId]) {
      console.warn(`🔁 Popup déjà affiché : ${popupId}`);
      return;
    }

    const popupElement = document.createElement("div");
    popupElement.className = "ia-popup";
    popupElement.innerHTML = contentHTML;

    popupElement.style.position = "fixed";
    popupElement.style.right = "20px";
    popupElement.style.bottom = `${20 + this.index * this.spacing}px`;
    popupElement.style.zIndex = 99999;

    document.body.appendChild(popupElement);
    window.THEDBOT_POPUP_CACHE[popupId] = true;
    this.index++;

    // 🔁 Fermeture automatique
    if (autoClose) {
      setTimeout(() => {
        this.closePopup(popupElement, popupId);
      }, duration);
    }

    // 🔘 Fermeture manuelle si #closeBtn
    const closeBtn = popupElement.querySelector("#closeBtn");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        this.closePopup(popupElement, popupId);
      });
    }
  },

  closePopup: function (popupElement, popupId) {
    if (popupElement && popupElement.parentNode) {
      popupElement.parentNode.removeChild(popupElement);
      delete window.THEDBOT_POPUP_CACHE[popupId];
      this.reorganizePopups();
    }
  },

  reorganizePopups: function () {
    const popups = document.querySelectorAll(".ia-popup");
    this.index = 0;
    popups.forEach((p) => {
      p.style.bottom = `${20 + this.index * this.spacing}px`;
      this.index++;
    });
  }
};

/**
 * 💡 Injection directe dans un conteneur graphique
 * Peut être appelée avec une zone DOM détectée dynamiquement
 */
window.injectPopup = function (container, index = 0, signalData = null) {
  const html = `
    <h4>🧠 Signal IA <span style="color:lime;">(${signalData?.direction || "BAS"})</span></h4>
    <p><strong>Score :</strong> ${signalData?.score || "78"}%</p>
    <p><strong>Contexte :</strong> ${signalData?.contexte || "Zone de résistance"}</p>
    <p><strong>Résumé :</strong> ${signalData?.resume || "Double top + divergence RSI"}</p>
    <p><strong>Fondamental :</strong> ${signalData?.fondamental || "Données neutres"}</p>
    <p><strong>💰 Mise :</strong> ${signalData?.mise || "3 USD"} – <strong>Durée :</strong> ${signalData?.duree || "120s"}</p>
    <button class="ia-btn">✅ Valider manuellement</button>
  `;
  window.PopupManager.showPopup(html, `signal_popup_${index}`, true, 20000);
};
