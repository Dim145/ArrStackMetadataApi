# Objectif
La stack arr (radarr, sonarr et lidarr) utilisent tous une api externe, non open-source et non-self-hostable
pour communiqué avec les APIs de leurs sources de metadonnées (tvdb, tmdb et musicbrainz).

Malgré le fait de self hosté ces projets arr, ils restent dépendant de ces APIs externes. Ces dernières peuvent aussi connaitres et enregistré de ce fait les données sur vos instances.  
De plus, ce proxy peut avoir des limitations ou tous simplement ne pas être disponible (comme celui de lidarr depuis plusieurs mois).

Pour éviter cela, j'ai créé ce projet qui permet de self hosté un équivalent de ces proxies en contactant directement les sources de données.

# Avancement
Le projet est en cours de dévelopment, il peut (et dois surement) être encore instable.

Les fonctionnalités implémentées sont les suivantes :
- [x] Sonarr:
  - [x] recherche de séries
  - [x] récupération des informations d'une série
  - [ ] recherche de series directement depuis une source de métadonnées
    - [x] tvdb
    - [ ] tmdb
    - [ ] anilist
    - [ ] mal
    - [ ] imdb
  - [ ] récupération des méta-données manquante depuis TVDB
    - [ ] l'horaire de sortie des épisodes
    - [ ] tvRageId
    - [ ] malIds
    - [ ] aniListIds
    - [ ] rating
- [x] Radarr:
  - [x] recherche de films
  - [x] récupération des informations d'un film
  - [x] récupération des informations d'une collection
  - [x] récupération des films popular (et "trending")
  - [x] récupération d'un film par son id imdb
  - [x] récupération des informations de plusieurs films par leurs id
  - [ ] optimisé les recherches pour ne pas faire de requêtes inutiles
  - [ ] récupération de méta-données manquantes depuis TMDB
    - [ ] certifications ?
    - [ ] other ratings 
- [ ] Lidarr:
  - [ ] recherche d'artistes
  - [ ] récupération des informations d'un artiste
  - [ ] recherche d'albums
  - [ ] récupération des informations d'un album
  - [ ] recherche de pistes
  - [ ] récupération des informations d'une piste
  - ... d'autres endpoints, je n'ai pas encore fait le tour

# Prérequis
Pour faire fonctionner ce projet, il est nécessaire de générer une clé api chez les différentes sources de 
métadonnées, voici les liens pour les générer :
- [The TVDB](https://thetvdb.com/api-information)
- [The Movie Database](https://developers.themoviedb.org/3/getting-started/introduction)
- [MusicBrainz](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2)

Pour le moment, **MusicBrainz**, n'est pas encore implémenté, mais il est prévu de l'être.

# Génération du certificat
Pour que le projet fonctionne, il est nécessaire de générer un certificat auto-signé, vous pouvez le faire avec la commande suivante :

```bash
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout cert.key -out cert.crt -subj "/C=FR/ST=France/L=Paris/O=MyCompany/CN=skyhook.sonarr.tv"
```

# Installation
Le projet est prévus pour fonctionner dans un container docker, il est donc nécessaire d'avoir docker et docker-compose d'installé.

Redis est requis pour le fonctionnement de ce projet, si vous n'avez pas de redis d'installé, vous pouvez le faire via docker-compose.

```yaml
services:
  metadata-server:
    image: ghcr.io/dim145/arrstackmetadataapi:latest
    container_name: metadata-server
    ports:
      - "8080:80"
    environment:
      TVDB_API_KEY: "xxx"
      TMDB_API_KEY: "xxx"
      METADATA_SERVER_FOR: "sonarr,radarr"
      REDIS_HOST: redis
      LANGS_FALLBACK: fra,eng
      INCLUDE_ADULT_CONTENT: false
    networks:
      - internal

  redis:
    image: redis:latest
    container_name: redis
    volumes:
      - redis_data:/data
    networks:
      - internal

# optionnel, pour avoir une interface graphique pour redis qui permet de géré le cache
  redis-insights:
    image: redis/redisinsight
    container_name: redis-insights
    ports:
      - '5540:5540'
    volumes:
      - redis_insights_data:/data
    depends_on:
      - redis
    networks:
      - internal

volumes:
  redis_data:
  redis_insights_data:

networks:
  internal:
    driver: bridge
    ipam:
      config:
        - subnet: 172.173.10.0/24
          gateway: 172.173.10.1
```

# Configuration
Pour que ce proxy soit utilisé par le projet arr, il va falloir changer un peu son yaml :

## Ajouter un proxy avec des certificats auto-signés au stack du proxy
### docker-compose du reverse proxy
```yaml
reverse-proxy:
    image: nginx:alpine
    networks:
      internal:
        ipv4_address: 172.173.10.100 # une ip statique est requise
    volumes:
      - ./docker-data/reverse-proxy:/etc/nginx/conf.d/ # emplacement du fichier de conf nginx (ci-dessous)
      - ./docker-data/certs:/certs # emplacement des certificats auto-signés
```
### Fichier metadata-server.conf  
Fichier à placer dans le dossier `/data/reverse-proxy` (ou l'emplacement que vous avez choisi dans le docker-compose du reverse proxy)
```
server {
  listen 443 ssl;

  ssl_certificate /certs/cert.crt;
  ssl_certificate_key /certs/cert.key;

  server_name skyhook.sonarr.tv;

  location / {
    set_real_ip_from 172.173.10.201/24;
    real_ip_header X-Forwarded-For;
    real_ip_recursive on;

    proxy_pass http://arr-metadata-proxy-server:80;
  }
}
```

## Ajouter les entrées suivantes dans le fichier docker-compose du projet arr
Exemple avec sonarr

### docker-compose de sonarr à modifier
```yaml
  sonarr:
    image: linuxserver/sonarr:version
    # ... reste de votre configuration
    volumes:
      # ... autres volumes
      - ./docker-data/certs/cert.crt:/usr/local/share/ca-certificates/cert.crt # ajoute juste le certificat auto-signé
      - ./docker-data/update-ca.sh:/custom-cont-init.d/update-ca.sh # script pour mettre à jour les certificats au démarrage du container
    extra_hosts: 
      # ... eventuels autres hosts
      - "skyhook.sonarr.tv:172.173.10.100" # l'ip du reverse proxy
```

### Script update-ca.sh
Le certificat auto-signé doit être ajouté aux certificats de confiance du container, pour cela, il faut ajouter un script qui sera exécuté au démarrage du container sonarr.
```bash
#!/bin/sh

update-ca-certificates

```