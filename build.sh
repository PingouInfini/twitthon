#!/usr/bin/env bash
rm -rf ./docker/context/dockerdist/*
touch ./docker/context/dockerdist/README.md
mkdir -p ./docker/context/dockerdist/src/ && cp -Rf ./src/* ./docker/context/dockerdist/src/
cp -Rf ./twitthon.iml ./docker/context/dockerdist/
cp -Rf ./twitthon.py ./docker/context/dockerdist/
cp -Rf ./setup.py ./docker/context/dockerdist/
cp -Rf ./entrypoint.sh ./docker/context/dockerdist/
cp -Rf ./requirements.txt ./docker/context/dockerdist/
cp -Rf ./twitter_credentials.txt ./docker/context/dockerdist/

docker-compose -f ./docker/twitthon.yml build
