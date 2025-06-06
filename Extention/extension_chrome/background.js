
let lastTrade = null;

async function fetchTrade() {
  try {
    const res = await fetch("http://localhost:8000/last_trade");
    const data = await res.json();
    if (data && data.symbol && data.symbol !== lastTrade?.symbol) {
      console.log("✅ Nouveau trade détecté:", data);
      lastTrade = data;
      executeTrade(data);
    }
  } catch (err) {
    console.error("❌ Erreur lors de la récupération du trade :", err);
  }
}

function executeTrade(data) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    if (tabs.length > 0) {
      chrome.scripting.executeScript({
        target: {tabId: tabs[0].id},
        func: (trade) => {
          alert("📈 Exécution du trade : " + JSON.stringify(trade));
          // Ici tu peux ajouter du DOM manipulation ou click simulation si nécessaire
        },
        args: [data]
      });
    }
  });
}

// Vérifie toutes les 5 secondes
setInterval(fetchTrade, 5000);
