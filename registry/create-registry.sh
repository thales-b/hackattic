#!/bin/bash
docker rm -f my-registry || true

docker run -d \
  -p 5000:5000 \
  --name my-registry \
  -v "$(pwd)/htpasswd:/etc/docker/registry/htpasswd" \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/etc/docker/registry/htpasswd" \
  registry:2
