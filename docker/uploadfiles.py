import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# --- Load .env file ---
load_dotenv()

REMOTE_USER = os.getenv("REMOTE_USER")
REMOTE_HOST = os.getenv("REMOTE_HOST")
REMOTE_PATH = os.getenv("REMOTE_PATH", "/root/codexion")
SSH_KEY = os.getenv("SSH_KEY")  # Optional

if not REMOTE_USER or not REMOTE_HOST:
    print("❌ REMOTE_USER or REMOTE_HOST missing from .env")
    exit(1)

# --- Files to Upload ---
FILES_TO_UPLOAD = [
    "docker-mariadb.yml",
    "securedb.sh",
    "getssl.sh",
    "uploadcertsremote.sh",
    "copycerts.sh",
    "sql_profile_codexion.xml",
    "init.sh"
]

# Include optional cert files if present
for cert_file in ["ca.pem", "server-cert.pem", "server-key.pem"]:
    if Path(cert_file).exists():
        FILES_TO_UPLOAD.append(cert_file)

# --- SSH base ---
ssh_base = ["ssh"]
scp_base = ["rsync", "-avz", "--progress"]

if SSH_KEY:
    ssh_base += ["-i", SSH_KEY]
    scp_base += ["-e", f"ssh -i {SSH_KEY}"]

ssh_base += [f"{REMOTE_USER}@{REMOTE_HOST}"]
scp_base.append("--")

# --- Verify SSH Connection ---
print("🔐 Checking SSH connection...")

try:
    subprocess.run(ssh_base + ["echo Connected ✅"], check=True)
except subprocess.CalledProcessError:
    print("❌ SSH connection failed. Check credentials or SSH key.")
    exit(1)

# --- Ensure remote path exists ---
print(f"📂 Creating remote folder: {REMOTE_PATH}")
subprocess.run(ssh_base + [f"mkdir -p {REMOTE_PATH}"], check=True)

# --- Upload files ---
for file in FILES_TO_UPLOAD:
    if Path(file).exists():
        print(f"📤 Uploading {file}")
        subprocess.run(scp_base + [file, f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}/"], check=True)
    else:
        print(f"⚠️  Skipping missing: {file}")

print(f"✅ All files uploaded to {REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}")
