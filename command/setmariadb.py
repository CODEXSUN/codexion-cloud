import os
import sys
from pathlib import Path
import subprocess
from dotenv import load_dotenv

# --------------------------------------
# Load .env for configuration
load_dotenv()

ssh_user = os.getenv("REMOTE_USER")
db_pass = os.getenv("MARIADB_ROOT_PASSWORD")
folder_name = os.getenv("FOLDER_NAME", "maridb")

if not ssh_user or not db_pass:
    print("❌ REMOTE_USER or MARIADB_ROOT_PASSWORD missing in .env")
    sys.exit(1)

# --------------------------------------
# Helper: Strip non-ASCII characters
def strip_unicode(text):
    return text.encode('ascii', 'ignore').decode('ascii')

# --------------------------------------
# Folder setup
base_path = Path.cwd() / folder_name
base_path.mkdir(parents=True, exist_ok=True)

# --------------------------------------
# File paths
compose_path = base_path / "docker-mariadb.yml"
secure_script_path = base_path / "securedb.sh"
cert_gen_script_path = base_path / "getssl.sh"
cert_upload_script_path = base_path / "uploadcertsremote.sh"
cert_copy_script_path = base_path / "copycerts.sh"
xml_path = base_path / "sql_profile.xml"
init_script_path = base_path / "init.sh"
usagemd_path = base_path / "usage.md"

# --------------------------------------
# docker-compose YAML
docker_compose = f"""
version: '3.8'

services:
  mariadb:
    image: mariadb:11.8
    container_name: codexion-db
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: {db_pass}
      MARIADB_SSL_CA: /certs/ca.pem
      MARIADB_SSL_CERT: /certs/server-cert.pem
      MARIADB_SSL_KEY: /certs/server-key.pem
    volumes:
      - db_data:/var/lib/mysql
      - /etc/mysql/certs:/certs:ro
    ports:
      - "3306:3306"

volumes:
  db_data:
"""

# --------------------------------------
# securedb.sh script
secure_script = f"""
#!/bin/bash

mysql -uroot -p'{db_pass}' -e "GRANT ALL PRIVILEGES ON *.* TO '{ssh_user}'@'%' IDENTIFIED BY '{db_pass}' WITH GRANT OPTION;"
mysql -uroot -p'{db_pass}' -e "FLUSH PRIVILEGES;"
"""

# --------------------------------------
# getssl.sh: Generate SSL certificates locally
cert_gen_script = """
#!/bin/bash

CERT_DIR = f"./{FOLDER_NAME}/certs"
mkdir -p "$CERT_DIR"

openssl genrsa 2048 > "$CERT_DIR/ca-key.pem"
openssl req -new -x509 -nodes -days 3650 -key "$CERT_DIR/ca-key.pem" -out "$CERT_DIR/ca.pem" -subj "/C=IN/ST=TN/L=Chennai/O=Codexion/CN=codexion.local"

openssl req -newkey rsa:2048 -days 3650 -nodes -keyout "$CERT_DIR/server-key.pem" -out "$CERT_DIR/server-req.pem" -subj "/C=IN/ST=TN/L=Chennai/O=Codexion/CN=codexion.local"
openssl rsa -in "$CERT_DIR/server-key.pem" -out "$CERT_DIR/server-key.pem"
openssl x509 -req -in "$CERT_DIR/server-req.pem" -days 3650 -CA "$CERT_DIR/ca.pem" -CAkey "$CERT_DIR/ca-key.pem" -set_serial 01 -out "$CERT_DIR/server-cert.pem"

openssl req -newkey rsa:2048 -days 3650 -nodes -keyout "$CERT_DIR/client-key.pem" -out "$CERT_DIR/client-req.pem" -subj "/C=IN/ST=TN/L=Chennai/O=Codexion/CN=client"
openssl rsa -in "$CERT_DIR/client-key.pem" -out "$CERT_DIR/client-key.pem"
openssl x509 -req -in "$CERT_DIR/client-req.pem" -days 3650 -CA "$CERT_DIR/ca.pem" -CAkey "$CERT_DIR/ca-key.pem" -set_serial 02 -out "$CERT_DIR/client-cert.pem"

ls -l "$CERT_DIR"
"""

# --------------------------------------
# uploadcertsremote.sh: Upload to server
cert_upload_script = f"""
#!/bin/bash

REMOTE_USER="{ssh_user}"
REMOTE_HOST="$1"
REMOTE_DIR="/etc/mysql/certs"
LOCAL_CERT_DIR="./certs"

ssh $REMOTE_USER@$REMOTE_HOST "sudo mkdir -p $REMOTE_DIR && sudo chown $REMOTE_USER:$REMOTE_USER $REMOTE_DIR"
scp $LOCAL_CERT_DIR/*.pem $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/
ssh $REMOTE_USER@$REMOTE_HOST "sudo chmod 600 $REMOTE_DIR/*.pem && sudo chown mysql:mysql $REMOTE_DIR/*.pem"
"""

# --------------------------------------
# copycerts.sh (legacy/manual fallback)
copy_certs_script = """
#!/bin/bash

mkdir -p /etc/mysql/ssl
cp /root/client-cert.pem /etc/mysql/ssl/
cp /root/client-key.pem /etc/mysql/ssl/
cp /root/ca-cert.pem /etc/mysql/ssl/
chown mysql:mysql /etc/mysql/ssl/*
chmod 600 /etc/mysql/ssl/*
"""

# --------------------------------------
# SQLyog profile
sql_profile = f"""
<?xml version=\"1.0\"?>
<Sessions>
  <Session>
    <Name>codexion</Name>
    <Host>127.0.0.1</Host>
    <Port>3306</Port>
    <User>root</User>
    <Password>{db_pass}</Password>
    <UseSSL>1</UseSSL>
    <SSL_CA>ca.pem</SSL_CA>
    <SSL_CERT>client-cert.pem</SSL_CERT>
    <SSL_KEY>client-key.pem</SSL_KEY>
  </Session>
</Sessions>
"""

# --------------------------------------
# init.sh to run all scripts
init_script = f"""
#!/bin/bash

bash getssl.sh
bash securedb.sh
bash uploadcertsremote.sh <REMOTE_IP>
"""

# --------------------------------------
# usage.md with instructions
usage_md = f"""
# Usage Guide

## 1. Generate Certificates
```bash
bash getssl.sh
```

## 2. Upload to Remote
```bash
bash uploadcertsremote.sh <remote_ip>
```

## 3. Run MariaDB
```bash
docker-compose -f docker-mariadb.yml up -d
```

## 4. Secure DB
```bash
bash securedb.sh
```

## 5. Import SQLyog Profile
Use `sql_profile.xml` to import into SQLyog.
"""

# --------------------------------------
# Write all files
files_to_write = [
    (compose_path, docker_compose),
    (secure_script_path, secure_script),
    (cert_gen_script_path, cert_gen_script),
    (cert_upload_script_path, cert_upload_script),
    (cert_copy_script_path, copy_certs_script),
    (xml_path, sql_profile),
    (init_script_path, init_script),
    (usagemd_path, usage_md)
]

for path, content in files_to_write:
    path.write_text(strip_unicode(content), encoding='utf-8')

# --------------------------------------
# Make shell scripts executable
for script in [secure_script_path, cert_gen_script_path, cert_upload_script_path, cert_copy_script_path, init_script_path]:
    subprocess.run(["chmod", "+x", str(script)], check=True)

print("\n✅ All files generated in:", base_path)
print("Run './init.sh <REMOTE_IP>' to start setup.")
