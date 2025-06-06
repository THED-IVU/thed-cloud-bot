// === Analyse IA via API locale ===
document.getElementById("analyzeBtn").addEventListener("click", () => {
  const status = document.getElementById("statusText");
  status.innerText = "⏳ Analyse en cours...";

  fetch("http://localhost:8000/analyse_strategique")
    .then(res => res.json())
    .then(data => {
      status.innerText = "✅ Analyse terminée. Résultat :\n" +
        JSON.stringify(data.resultat || data, null, 2);
    })
    .catch(err => {
      console.error(err);
      status.innerText = "❌ Erreur lors de l’analyse IA.";
    });
});

// === Signal IA prédéfini (exemple) ===
const signal = {
  direction: "HAUT",
  score: 91,
  resume: "Croisement EMA 9/21 confirmé par RSI 60+",
  fondamental: "Aucune nouvelle économique bloquante.",
  mise: "5 USD",
  duree: "1m"
};

// Injection des infos dans la popup HTML
document.getElementById("iaScore").innerText = `${signal.score} %`;
document.getElementById("iaDirection").innerText = signal.direction;
document.getElementById("resumeTechnique").innerText = signal.resume;
document.getElementById("resumeFondamentale").innerText = signal.fondamental;
document.getElementById("paramMise").innerText = signal.mise;
document.getElementById("paramDuree").innerText = signal.duree;

// Mode TEST ou RÉEL
const mode = sessionStorage.getItem("isRealMode") === "true" ? "RÉEL" : "TEST";
document.getElementById("currentMode").innerText = mode;

// Envoi via WebSocket
document.getElementById("validerBtn").addEventListener("click", () => {
  const ws = new WebSocket("ws://localhost:8765");
  ws.onopen = () => {
    ws.send(JSON.stringify({ type: "SIGNAL_FROM_POPUP", payload: signal }));
  };
  alert("Signal IA envoyé au bot !");
});
