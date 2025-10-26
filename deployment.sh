#!/bin/bash
containers=$(docker ps -aq)
images=$(docker images -a )
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q )
docker build -t msp-backend:latest .
docker run -d --name msp-backend-container -p 8000:8000 msp-backend:latest