
chrome.runtime.onInstalled.addListener(() => {
    console.log("THED IVU Bot Extension installée.");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "EXECUTE_TRADE") {
        fetch("http://localhost:8000/send_trade", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(message.data)
        })
        .then(res => res.json())
        .then(json => console.log("Réponse API:", json))
        .catch(err => console.error("Erreur:", err));
    }
});
