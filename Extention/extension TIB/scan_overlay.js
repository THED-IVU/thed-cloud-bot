// 📁 Fichier : scan_overlay.js

window.launchScanEffect = function () {
  if (document.querySelector("#thed-scan-overlay")) return; // évite doublons

  const overlay = document.createElement("div");
  overlay.id = "thed-scan-overlay";
  overlay.style.position = "fixed";
  overlay.style.top = "0";
  overlay.style.left = "0";
  overlay.style.width = "100%";
  overlay.style.height = "100%";
  overlay.style.pointerEvents = "none";
  overlay.style.zIndex = "999999";
  overlay.style.background = "linear-gradient(120deg, rgba(0,255,255,0.05) 0%, rgba(0,255,255,0.2) 50%, rgba(0,255,255,0.05) 100%)";
  overlay.style.animation = "scanFluo 2s linear infinite";

  const style = document.createElement("style");
  style.innerHTML = `
    @keyframes scanFluo {
      0% { transform: translateY(-100%); opacity: 0.3; }
      50% { transform: translateY(0%); opacity: 0.6; }
      100% { transform: translateY(100%); opacity: 0.3; }
    }
  `;

  document.head.appendChild(style);
  document.body.appendChild(overlay);

  // disparition après 10 secondes
  setTimeout(() => {
    overlay.remove();
    style.remove();
  }, 10000);
};
