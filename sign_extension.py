import os
import zipfile
import subprocess

# === CONFIGURATION ===
EXTENSION_DIR = "chrome_extension"  # Dossier où se trouvent manifest.json, popup.html, etc.
PRIVATE_KEY_FILE = "private_key.pem"  # Clé privée pour la signature (à générer une fois)
OUTPUT_CRX = "thed_ivu_bot.crx"

# === CRX HEADER MAGIC ===
CRX_HEADER = b'Cr24'
VERSION = (3).to_bytes(4, byteorder='little')  # CRX3

def generate_key():
    print("🔑 Génération de la clé privée...")
    subprocess.run(["openssl", "genrsa", "-out", PRIVATE_KEY_FILE, "2048"], check=True)
    print("✅ Clé générée :", PRIVATE_KEY_FILE)

def zip_extension():
    zip_name = "extension.zip"
    print("📦 Compression des fichiers de l'extension...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, _, filenames in os.walk(EXTENSION_DIR):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, EXTENSION_DIR)
                zipf.write(filepath, arcname)
    return zip_name

def generate_crx(zip_path):
    print("🔏 Signature du CRX...")
    # Signature avec OpenSSL
    signed_file = "signature.sig"
    subprocess.run(["openssl", "dgst", "-sha256", "-sign", PRIVATE_KEY_FILE, "-out", signed_file, zip_path], check=True)

    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key = f.read()
    with open(signed_file, "rb") as f:
        signature = f.read()
    with open(zip_path, "rb") as f:
        zip_content = f.read()

    # Construction du fichier CRX3
    header = (
        CRX_HEADER +
        VERSION +
        len(signature).to_bytes(4, byteorder='little') +
        len(zip_content).to_bytes(4, byteorder='little')
    )

    with open(OUTPUT_CRX, "wb") as crx:
        crx.write(header)
        crx.write(signature)
        crx.write(zip_content)

    print(f"✅ Extension signée : {OUTPUT_CRX}")

if __name__ == "__main__":
    if not os.path.exists(PRIVATE_KEY_FILE):
        generate_key()

    zip_path = zip_extension()
    generate_crx(zip_path)
