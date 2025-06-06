
let lastTrade = null;

async function fetchTrade() {
  try {
    const res = await fetch("http://localhost:8000/last_trade");
    const data = await res.json();
    if (data && data.symbol && data.symbol !== lastTrade?.symbol) {
      console.log("✅ Nouveau trade reçu :", data);
      lastTrade = data;
      executeTrade(data);
    }
  } catch (err) {
    console.error("❌ Erreur récupération trade :", err);
  }
}

function executeTrade(data) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    if (tabs.length > 0) {
      chrome.scripting.executeScript({
        target: {tabId: tabs[0].id},
        func: (trade) => {
          alert("🚀 Exécution du trade IA : " + JSON.stringify(trade));
        },
        args: [data]
      });
    }
  });
}

// Vérification périodique toutes les 5 secondes
setInterval(fetchTrade, 5000);
