#!/bin/bash

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

#for alpine clean everything
git reset --hard && git clean -dfx
git checkout tags/"${TRAVIS_TAG}" -b "${TRAVIS_TAG}"

#alpine
docker build . -t dinutac/jinja2docker:"${TRAVIS_TAG}"
docker push dinutac/jinja2docker:"${TRAVIS_TAG}"