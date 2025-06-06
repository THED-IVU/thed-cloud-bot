// injector.js – Injection automatique de popups IA dans Pocket Option

(function () {
  console.log("🧠 THED IVU BOT – Injection dans Pocket Option...");

  // === Partie 1 : Injection statique de test (affiche un popup simple)
  const signal = {
    direction: "HAUT",
    score: 88,
    contexte: "Breakout confirmé",
    resume: "EMA croisé + MACD + RSI",
    fondamental: "Pas d'obstacle fondamental",
    mise: "3 USD",
    duree: "120s"
  };

  function injectPopup(signalData) {
    const popup = document.createElement("div");
    popup.classList.add("ia-popup");
    popup.style.position = "fixed";
    popup.style.bottom = "20px";
    popup.style.right = "20px";
    popup.style.background = "#2962ff";
    popup.style.color = "white";
    popup.style.padding = "12px";
    popup.style.borderRadius = "8px";
    popup.style.boxShadow = "0 2px 6px rgba(0,0,0,0.3)";
    popup.style.zIndex = "99999";
    popup.style.fontSize = "14px";
    popup.innerHTML = `
      <b>📈 Signal IA</b><br>
      Direction : ${signalData.direction}<br>
      Score : ${signalData.score}%<br>
      Mise : ${signalData.mise} – Durée : ${signalData.duree}
    `;
    PopupManager.showPopup(popup, signal.id || `popup_${Date.now()}`);
    setTimeout(() => popup.remove(), 15000);
  }

  injectPopup(signal);

  // === Partie 2 : Popups multiples simulées manuellement
  const signaux = [
    {
      id: "popup1",
      direction: "HAUT",
      score: 87,
      contexte: "Retournement haussier",
      resume: "EMA 9/21 croisé + RSI > 50",
      fondamental: "Pas de news négative",
      mise: "2 USD",
      duree: "60s"
    },
    {
      id: "popup2",
      direction: "BAS",
      score: 78,
      contexte: "Zone de résistance",
      resume: "Double top + divergence RSI",
      fondamental: "Données neutres",
      mise: "3 USD",
      duree: "120s"
    }
  ];

  function createSimulatedPopup(signal, index) {
    const popup = document.createElement("div");
    popup.classList.add("ia-popup");
    popup.style.position = "fixed";
    popup.style.bottom = `${80 + index * 140}px`;
    popup.style.right = "20px";
    popup.style.width = "300px";
    popup.style.background = "#1c1c1c";
    popup.style.border = "1px solid #444";
    popup.style.borderRadius = "10px";
    popup.style.padding = "10px";
    popup.style.boxShadow = "0 0 12px #00f7ff";
    popup.style.zIndex = "9999";
    popup.style.color = "#fff";
    popup.style.fontFamily = "Segoe UI";
    popup.innerHTML = `
      <h4 style="color:#00f7ff;">📊 Signal IA (${signal.direction})</h4>
      <p><strong>Score :</strong> ${signal.score}%</p>
      <p><strong>Contexte :</strong> ${signal.contexte}</p>
      <p><strong>Résumé :</strong><br><em>${signal.resume}</em></p>
      <p><strong>Fondamental :</strong><br><em>${signal.fondamental}</em></p>
      <p>💰 <strong>Mise :</strong> ${signal.mise} – <strong>Durée :</strong> ${signal.duree}</p>
      <button id="valider_${signal.id}" style="background:#ffa500;color:white;border:none;padding:8px 12px;border-radius:6px;margin-top:8px;cursor:pointer;">
        ✅ Valider manuellement
      </button>
    `;
    PopupManager.showPopup(popup, signal.id || `popup_${Date.now()}`);

    document.getElementById(`valider_${signal.id}`).addEventListener("click", () => {
      const message = {
        type: "SIGNAL_MANUEL_VALIDÉ",
        payload: signal
      };

      console.log("📤 Signal IA validé :", message);

      try {
        const ws = new WebSocket("ws://localhost:8765");
        ws.onopen = () => {
          ws.send(JSON.stringify(message));
        };
      } catch (e) {
        console.warn("❌ WebSocket non disponible :", e);
      }

      alert(`🚀 Signal ${signal.direction} envoyé avec succès !`);
    });
  }

  signaux.forEach((s, i) => createSimulatedPopup(s, i));

  // === Partie 3 : Réception live via WebSocket + template HTML
  (async function () {
    try {
      const templateUrl = chrome.runtime.getURL("popup_template.html");
      const templateHTML = await fetch(templateUrl).then(res => res.text());

      const ws = new WebSocket("ws://localhost:8765");
      ws.onopen = () => console.log("✅ WebSocket IA connecté");

      ws.onmessage = (event) => {
        const signal = JSON.parse(event.data);
        if (!signal || !signal.direction) return;

        const id = `popup_${Date.now()}`;
        const wrapper = document.createElement("div");
        wrapper.innerHTML = templateHTML;

        const popup = wrapper.firstElementChild;
        popup.style.position = "fixed";
        popup.style.right = "20px";
        popup.style.bottom = `${Math.random() * 300 + 50}px`;
        popup.style.zIndex = 9999;
        popup.id = id;

        popup.querySelector("#dir").innerText = signal.direction || "–";
        popup.querySelector("#score").innerText = signal.score || "–";
        popup.querySelector("#contexte").innerText = signal.contexte || "–";
        popup.querySelector("#resume").innerText = signal.resume || "–";
        popup.querySelector("#fondamental").innerText = signal.fondamental || "–";
        popup.querySelector("#mise").innerText = signal.mise || "–";
        popup.querySelector("#duree").innerText = signal.duree || "–";

        popup.querySelector("#validerBtn").addEventListener("click", () => {
          ws.send(JSON.stringify({ type: "SIGNAL_MANUEL_VALIDÉ", payload: signal }));
          alert("🚀 Signal IA validé (WebSocket)");
        });

        PopupManager.showPopup(popup, signal.id || `popup_${Date.now()}`);
      };
    } catch (err) {
      console.warn("❌ Échec de chargement WebSocket ou template :", err);
    }
  })();

  // === Partie 4 : Injection automatique en MutationObserver
  console.log("🔁 Injection de l’IA THED BOT en cours…");
  window.injectPopup = injectPopup;

  window.addEventListener("load", () => {
    const observer = new MutationObserver(() => {
      const containers = document.querySelectorAll(".trade-view, .chart, .main-content");
      containers.forEach((container, index) => {
        if (!container.querySelector(".ia-popup")) {
          window.injectPopup(signal, index);
        }
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });

    if (typeof window.launchScanEffect === "function") {
      window.launchScanEffect();
    }
  });
})();
"content_scripts": [
  {
    "matches": ["https://po.trade/*"],
    "js": ["injector.js", "popup_manager.js", "scan_overlay.js"],
    "css": ["styles.css"],
    "run_at": "document_idle"
  }
]
