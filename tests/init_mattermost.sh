#!/bin/bash

docker-compose up -d

# Wait for Mattermost
sleep 5

docker-compose exec platform user create --email errbot@example.com --username errbot --password errbot
docker-compose exec platform user verify errbot