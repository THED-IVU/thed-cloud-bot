// 📡 webSocket_listener.js – Récepteur de signaux IA via WebSocket pour Extension THED IVU BOT

(function () {
  console.log("🔌 Connexion IA – WebSocket Listener initialisé.");

  let autoMode = false;

  // 🔁 Bouton de mode manuel / automatique
  const switchBtn = document.createElement("button");
  switchBtn.textContent = "🔁 Mode : Manuel";
  Object.assign(switchBtn.style, {
    position: "fixed",
    top: "10px",
    left: "10px",
    zIndex: 100000,
    padding: "6px 10px",
    background: "#222",
    color: "lime",
    border: "1px solid lime",
    borderRadius: "8px",
    cursor: "pointer"
  });

  switchBtn.onclick = () => {
    autoMode = !autoMode;
    switchBtn.textContent = autoMode ? "🤖 Mode : Auto" : "🔁 Mode : Manuel";
    switchBtn.style.background = autoMode ? "#004400" : "#222";
  };
  document.body.appendChild(switchBtn);

  // 🟢 Icône d’état IA flottante
  const iaStatus = document.createElement("div");
  iaStatus.innerHTML = "🧠 IA ACTIVE";
  Object.assign(iaStatus.style, {
    position: "fixed",
    bottom: "10px",
    right: "10px",
    background: "#111",
    color: "lime",
    padding: "4px 10px",
    borderRadius: "8px",
    zIndex: 100000,
    fontSize: "12px",
    fontWeight: "bold",
    boxShadow: "0 0 8px lime"
  });
  document.body.appendChild(iaStatus);

  const socket = new WebSocket("ws://localhost:8777");

  socket.onopen = () => console.log("✅ WebSocket connecté à localhost:8777");
  socket.onerror = error => console.error("❌ Erreur WebSocket :", error);

  socket.onmessage = function (event) {
    try {
      const data = JSON.parse(event.data);
      console.log("📩 Signal IA reçu :", data);

      // Score pondéré
      const score_total = Math.round((data.score * 0.7) + (data.fondamental?.includes("Pas de news") ? 30 : 10));

      // Indicateurs utilisés
      const indicateurs_utilises = data.resume?.match(/(RSI|MACD|EMA\d+|Stoch|Bollinger)/g)?.join(", ") || "Indicateurs non précisés";

      const popupHTML = `
        <h4>🧠 Signal IA <span style="color:${data.direction === "HAUT" ? "lime" : "red"};">(${data.direction})</span></h4>
        <p><strong>Score Technique :</strong> ${data.score}%</p>
        <p><strong>Score Pondéré :</strong> ${score_total}%</p>
        <p><strong>Contexte :</strong> ${data.contexte}</p>
        <p><strong>Résumé :</strong> ${data.resume}</p>
        <p><strong>Indicateurs :</strong> ${indicateurs_utilises}</p>
        <p><strong>Fondamental :</strong> ${data.fondamental}</p>
        <p><strong>💰 Mise :</strong> ${data.mise} – <strong>Durée :</strong> ${data.duree}</p>
        <button class="ia-btn" id="validerBtn_${data.timestamp}">✅ Valider manuellement</button>
      `;

      // Historique
      const historique = JSON.parse(localStorage.getItem("thedbot_signaux") || "[]");
      historique.unshift({ ...data, score_total, indicateurs_utilises });
      localStorage.setItem("thedbot_signaux", JSON.stringify(historique.slice(0, 50)));

      // Afficher le popup
      if (window.PopupManager?.showPopup) {
        const id = `popup_${data.timestamp}`;
        window.PopupManager.showPopup(popupHTML, id, false, 30000);

        setTimeout(() => {
          const btn = document.querySelector(`#validerBtn_${data.timestamp}`);
          if (btn) {
            btn.addEventListener("click", () => envoyerOrdre(data));
          }
          if (autoMode) {
            envoyerOrdre(data);
          }
        }, 100);
      }
    } catch (e) {
      console.error("❌ Erreur parsing WS :", e);
    }
  };

  function envoyerOrdre(data) {
    console.log("📤 Envoi vers API Flask :", data);
    fetch("http://localhost:8000/send_trade", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    })
      .then(res => {
        if (!res.ok) throw new Error(`Erreur HTTP ${res.status}`);
        return res.json ? res.json() : {};
      })
      .then(result => console.log("✅ Réponse API :", result))
      .catch(err => console.error("❌ Erreur d'envoi :", err));
  }
})();
