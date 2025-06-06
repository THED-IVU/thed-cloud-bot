// === interact_buttons.js ===
// Contrôle automatique des trades sur Pocket Option selon signal IA
// Injecté via extension (Chrome/Opera/Firefox), DOM + WebSocket + toggle réel/test

let modeExecutionReel = false; // ✅ Faux par défaut (mode TEST)

// 🎯 Détecter le type de trading (binaire / forex)
function detectMode() {
  const url = window.location.href;
  if (url.includes("/quick-high-low")) return "binaire";
  if (url.includes("/mt5") || url.includes("/mt4")) return "forex";
  return null;
}

// 🔵 TRADE BINAIRE : CALL / PUT
function executeBinaryTrade(direction, duration = 60) {
  const selector = direction === "up" ? "div.button-call" : "div.button-put";
  const button = document.querySelector(selector);
  if (button) {
    if (modeExecutionReel) {
      button.click(); // 🟢 Action réelle
    }
    notifyUser(`✅ Trade binaire ${modeExecutionReel ? "RÉEL" : "TEST"} : ${direction}`);
    console.log("💥 Binaire :", direction);
  } else {
    notifyUser(`❌ Bouton binaire non trouvé pour : ${direction}`);
    console.warn("❌ Bouton binaire manquant.");
  }
}

// 🟠 TRADE FOREX : BUY / SELL avec SL/TP
function executeForexTrade(direction, stopLoss = 0, takeProfit = 0) {
  const btn = direction === "up"
    ? document.querySelector("button.btn-buy")
    : document.querySelector("button.btn-sell");

  if (btn) {
    if (modeExecutionReel) {
      const slField = document.querySelector('input[placeholder="Stop Loss, $"]');
      const tpField = document.querySelector('input[placeholder="Take Profit, $"]');
      if (slField) slField.value = stopLoss;
      if (tpField) tpField.value = takeProfit;
      btn.click(); // 🟢 Action réelle
    }
    notifyUser(`✅ Trade forex ${modeExecutionReel ? "RÉEL" : "TEST"} : ${direction}`);
    console.log("💥 Forex :", direction);
  } else {
    notifyUser(`❌ Bouton forex non trouvé pour : ${direction}`);
    console.warn("❌ Bouton forex manquant.");
  }
}

// 🧠 Lancement automatique d’un trade depuis un signal IA
function launchAutoTrade(signal) {
  const mode = detectMode();
  if (!mode) return notifyUser("❌ Mode de trading non reconnu.");

  const direction = signal.direction || "up";
  const duree = signal.duree || 60;
  const stop = signal.stop || 0;
  const tp = signal.tp || 0;

  if (mode === "binaire") {
    executeBinaryTrade(direction, duree);
  } else if (mode === "forex") {
    executeForexTrade(direction, stop, tp);
  } else {
    notifyUser("⚠️ Mode de trading non supporté.");
  }

  // 🔁 Logger local (optionnel)
  try {
    console.log("📦 Log signal :", signal);
  } catch (err) {
    console.warn("📛 Erreur log signal :", err);
  }
}

// 🔔 Affichage popup (notification debug)
function notifyUser(message) {
  const existing = document.getElementById("trade-alert");
  if (existing) existing.remove();

  const popup = document.createElement("div");
  popup.id = "trade-alert";
  popup.innerText = message;
  popup.style.position = "fixed";
  popup.style.top = "20px";
  popup.style.right = "20px";
  popup.style.padding = "12px";
  popup.style.backgroundColor = "#1f1f1f";
  popup.style.color = "#fff";
  popup.style.border = "2px solid limegreen";
  popup.style.borderRadius = "8px";
  popup.style.zIndex = "99999";
  document.body.appendChild(popup);
  setTimeout(() => popup.remove(), 4000);
}

// 🔄 Synchronisation avec le mode (popup.js)
chrome.storage.local.get(["isRealMode"], (result) => {
  modeExecutionReel = result.isRealMode || false;
  console.log("🛠 Mode détecté :", modeExecutionReel ? "RÉEL" : "TEST");
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "TOGGLE_MODE") {
    modeExecutionReel = msg.payload;
    console.log("🔁 Mode changé dynamiquement :", modeExecutionReel ? "RÉEL" : "TEST");
    sendResponse("✅ Mode mis à jour dans interact_buttons.js");
  }
});

// 🌐 Connexion WebSocket à l'IA locale
function initWebSocketConnection() {
  const ws = new WebSocket("ws://localhost:8765");

  ws.onopen = () => {
    console.log("🟢 WebSocket connecté.");
    notifyUser("🧠 Extension connectée à IA (WebSocket)");
  };

  ws.onmessage = (event) => {
    try {
      const signal = JSON.parse(event.data);
      console.log("📥 Signal IA reçu :", signal);
      launchAutoTrade(signal);
    } catch (e) {
      console.warn("⚠️ Erreur parsing signal WebSocket :", e);
    }
  };

  ws.onerror = (error) => {
    console.error("❌ Erreur WebSocket :", error);
    notifyUser("❌ Connexion WebSocket impossible");
  };

  ws.onclose = () => {
    console.warn("🔌 WebSocket fermé.");
    setTimeout(initWebSocketConnection, 3000); // Retry automatique
  };
}

// 🚀 Initialisation automatique après injection
setTimeout(() => {
  initWebSocketConnection(); // 📡 Connexion bot IA
}, 2000);
