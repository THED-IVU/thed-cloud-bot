// background.js – THED IVU BOT Extension

// 🔄 À l'installation de l'extension
chrome.runtime.onInstalled.addListener(() => {
  console.log("🧠 THED IVU BOT installé.");
});

// 🔘 Quand l'utilisateur clique sur l'icône de l'extension
chrome.action.onClicked.addListener((tab) => {
  console.log("🔘 Icône cliquée sur :", tab.url);
});

// 📡 Écoute des messages entrants (popup → background)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "EXECUTE_TRADE") {
    fetch("http://localhost:8000/send_trade", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(message.data)
    })
      .then(res => res.json())
      .then(json => console.log("✅ Réponse API:", json))
      .catch(err => console.error("❌ Erreur:", err));
  }
});
