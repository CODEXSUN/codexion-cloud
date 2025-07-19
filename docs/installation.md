
```
git clone https://github.com/CODEXSUN/codexion-cloud.git
```

```
docker network create codexion-network
```

# mariadb

```
rm -rf docker-mariadb.yml
```
```
nano docker-mariadb.yml
```

```
services:
  mariadb:
    image: mariadb:11.8
    container_name: codexion-db
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: DbPass1@@
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "3306:3306"
    networks:
      - codexion-network

volumes:
  db_data:

networks:
  codexion-network:
    external: true
```

```
docker compose -f docker-mariadb.yml up -d --build
```

```
docker exec -it codexion-db bash
```

```
docker ps -a
```




# Post Gress

```
rm -rf docker-pg.yml
```
```
nano docker-pg.yml
```

```
services:
  postgres:
    image: postgres:16
    container_name: codexion-pg
    restart: unless-stopped
    environment:
      POSTGRES_USER: codexion
      POSTGRES_PASSWORD: DbPass1@@
      POSTGRES_DB: codexion_db
    volumes:
      - pg_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - codexion-network

volumes:
  pg_data:

networks:
  codexion-network:
    external: true

```

```
docker compose -f docker-pg.yml up -d --build
```

```
docker exec -it codexion-pg bash
```









# soft Aaran : 8000

```
docker stop soft_aaran_org
```
```
docker rm soft_aaran_org
```
```
docker rmi soft_aaran_org
```


```
rm -rf docker-soft_aaran.yml
```
```
nano docker-soft_aaran.yml
```

```
services:
  soft_aaran_com:
    build:
      context: .
      dockerfile: Dockerfile
    image: soft_aaran:v1
    container_name: soft_aaran_org
    ports:
      - "8000:8000"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.soft_aaran_org.rule=Host(`soft.aaran.org`)"
      - "traefik.http.routers.soft.entrypoints=web"
      - "traefik.http.routers.soft_aaran_org.entrypoints=websecure"
      - "traefik.http.routers.soft_aaran_org.tls.certresolver=myresolver"
      - "traefik.http.services.soft.loadbalancer.server.port=8000"
    networks:
      - codexion-network
    restart: unless-stopped
    tty: true

networks:
  codexion-network:
    external: true
```

```
docker compose -f docker-soft_aaran.yml up -d --build
```

```
docker exec -it soft_aaran_org bash
```

---
### sukraa garments : 8001


```
docker stop sukraa_aaranerp_com
```
```
docker rm sukraa_aaranerp_com
```
```
docker rmi sukraa:v1
```

```
rm -rf docker-sukraa.yml
```
```
nano docker-sukraa.yml
```

```
services:
  sukraa_aaranerp_com:
    build:
      context: .
      dockerfile: Dockerfile
    image: sukraa:v1
    container_name: sukraa_aaranerp_com
    ports:
      - "8001:8000"  # Only for direct IP:8001 access, optional for Traefik
    labels:
      - "traefik.enable=true"

      # 🟩 HTTP (port 80) Router
      - "traefik.http.routers.sukraa.rule=Host(`sukraa.aaranerp.com`)"
      - "traefik.http.routers.sukraa.entrypoints=web"
      - "traefik.http.services.sukraa.loadbalancer.server.port=8000"

      # 🟦 HTTPS (port 443) Router with TLS
      - "traefik.http.routers.sukraa-secure.rule=Host(`sukraa.aaranerp.com`)"
      - "traefik.http.routers.sukraa-secure.entrypoints=websecure"
      - "traefik.http.routers.sukraa-secure.tls=true"
      - "traefik.http.routers.sukraa-secure.tls.certresolver=myresolver"
      - "traefik.http.services.sukraa-secure.loadbalancer.server.port=8000"

    networks:
      - codexion-network
    restart: unless-stopped
    tty: true

networks:
  codexion-network:
    external: true
```


```
docker compose -f docker-sukraa.yml up -d --build
```

```
docker exec -it sukraa_aaranerp_com bash
```

---

# Sk printers : 8002


```
rm -rf docker-skprinters.yml
```
```
nano docker-skprinters.yml
```

```
services:
  skprinters_aaranerp_com:
    build:
      context: .
      dockerfile: Dockerfile
    image: skprinters:v1
    container_name: skprinters_aaranerp_com
    ports:
      - "8002:8000"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.skprinters-aranerp-com.rule=Host(`skprinters.aaranerp.com`)"
      - "traefik.http.routers.skprinters-aranerp-com.entrypoints=websecure"
      - "traefik.http.routers.skprinters-aranerp-com.tls.certresolver=myresolver"
    networks:
      - codexion-network
    restart: unless-stopped
    tty: true

networks:
  codexion-network:
    external: true
```


```
docker compose -f docker-skprinters.yml up -d --build
```

```
docker exec -it skprinters_aaranerp_com bash
```

---

# ganapathi : 8003

```
rm -rf docker-ganapathi.yml
```
```
nano docker-ganapathi.yml
```

```
services:
  ganapathi_aaranerp_com:
    build:
      context: .
      dockerfile: Dockerfile
    image: ganapathi:v1
    container_name: ganapathi_aaranerp_com
    ports:
      - "8003:8000"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ganapathi-aranerp-com.rule=Host(`ganapathi.aaranerp.com`)"
      - "traefik.http.routers.ganapathi-aranerp-com.entrypoints=websecure"
      - "traefik.http.routers.ganapathi-aranerp-com.tls.certresolver=myresolver"
    networks:
      - codexion-network
    restart: unless-stopped
    tty: true

networks:
  codexion-network:
    external: true
```

```
docker compose -f docker-ganapathi.yml up -d --build
```

```
docker exec -it ganapathi_aaranerp_com bash
```


---

# Flex Con : 8004


```
rm -rf docker-flexcon.yml
```
```
nano docker-flexcon.yml
```

```
services:
  flexcon_aaranerp_com:
    build:
      context: .
      dockerfile: Dockerfile
    image: flexcon:v1
    container_name: flexcon_aaranerp_com
    ports:
      - "8004:8000"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.flexcon-aranerp-com.rule=Host(`flexcon.aaranerp.com`)"
      - "traefik.http.routers.flexcon-aranerp-com.entrypoints=websecure"
      - "traefik.http.routers.flexcon-aranerp-com.tls.certresolver=myresolver"
    networks:
      - codexion-network
    restart: unless-stopped
    tty: true

networks:
  codexion-network:
    external: true
```

```
docker compose -f docker-flexcon.yml up -d --build
```

```
docker exec -it fkexcon_aaranerp_com bash
```

# Prortainer
---

```
rm -rf docker-portainer.yml
```

```
nano docker-portainer.yml
```

```
services:
  portainer:
    image: portainer/portainer-ce:2.20.3
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9001:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    networks:
      - codexion-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.portainer.rule=Host(`porter.aaran.org`)"
      - "traefik.http.routers.portainer.entrypoints=websecure"
      - "traefik.http.routers.portainer.tls.certresolver=myresolver"
      - "traefik.http.services.portainer.loadbalancer.server.port=9000"

volumes:
  portainer_data:

networks:
  codexion-network:
    external: true

```

```
docker compose -f docker-portainer.yml up -d --build
```

```
docker exec -it portainer_aaran_org bash
```


# traefik
---

```
rm -rf docker-traefik.yml
```

```
nano docker-traefik.yml
```

```
services:
  traefik:
    image: traefik:v2.11.0
    container_name: traefik
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=admin@aaran.org"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.rule=Host(`traf.aaran.org`)"
      - "traefik.http.routers.traefik.entrypoints=websecure"
      - "traefik.http.routers.traefik.tls.certresolver=myresolver"
      - "traefik.http.routers.traefik.service=api@internal"
      - "traefik.http.routers.traefik.middlewares=https-redirect"
      - "traefik.http.middlewares.https-redirect.redirectscheme.scheme=https"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "./letsencrypt:/letsencrypt"
    networks:
      - codexion-network
    restart: unless-stopped

networks:
  codexion-network:
    external: true

```

```
docker compose -f docker-traefik.yml up -d --build
```

```
docker exec -it traefik bash
```

```
touch ./letsencrypt/acme.json
chmod 600 ./letsencrypt/acme.json

```

porter.aaran.org



docker stop sukraa_aaranerp_com
docker rm sukraa_aaranerp_com
docker rmi sukraa:v1


b54cd57e3771   portainer/portainer-ce:2.20.3   "/portainer"             About an hour ago   Up About an hour   8000/tcp, 9443/tcp, 0.0.0.0:9001->9000/tcp, [::]:9001->9000/tcp                                                             portainer
a6d547904f51   traefik:v2.11.0                 "/entrypoint.sh --ap…"   About an hour ago   Up About an hour   0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:443->443/tcp, [::]:443->443/tcp, 0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   traefik
7d7b99133efb   flexcon:v1                      "/usr/bin/supervisor…"   About an hour ago   Up About an hour   8080/tcp, 8888/tcp, 9000/tcp, 0.0.0.0:8004->8000/tcp, [::]:8004->8000/tcp                                                   flexcon_aaranerp_com
a8e8dbcf2369   ganapathi:v1                    "/usr/bin/supervisor…"   About an hour ago   Up About an hour   8080/tcp, 8888/tcp, 9000/tcp, 0.0.0.0:8003->8000/tcp, [::]:8003->8000/tcp                                                   ganapathi_aaranerp_com
c459d0ca2e46   skprinters:v1                   "/usr/bin/supervisor…"   2 hours ago         Up 2 hours         8080/tcp, 8888/tcp, 9000/tcp, 0.0.0.0:8002->8000/tcp, [::]:8002->8000/tcp                                                   skprinters_aaranerp_com
a0b874969941   sukraa:v1                       "/usr/bin/supervisor…"   2 hours ago         Up 2 hours         8080/tcp, 8888/tcp, 9000/tcp, 0.0.0.0:8001->8000/tcp, [::]:8001->8000/tcp                                                   sukraa_aaranerp_com
55b72da15728   soft_aaran:v1                   "/usr/bin/supervisor…"   2 hours ago         Up 2 hours         8080/tcp, 8888/tcp, 0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 9000/tcp                                                   soft_aaran_org
e3f44922daf4   postgres:16                     "docker-entrypoint.s…"   2 hours ago         Up 2 hours         0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                                                                                 codexion-pg
0be121e6cca7   mariadb:11.8                    "docker-entrypoint.s…"   2 hours ago         Up 2 hours         0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp                                                                                 codexion-db