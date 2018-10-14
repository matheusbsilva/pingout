#!/bin/bash

set -e

docker build -t gcr.io/${PROJECT_ID}/${PINGOUT_IMAGE}:$TRAVIS_COMMIT .

# Turn key to service auth json
echo $GCLOUD_SERVICE_KEY_STG | base64 --decode -i > ${HOME}/gcloud-service-key.json

gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json

gcloud --quiet config set project $PROJECT_ID
gcloud --quiet config set container/cluster $CLUSTER 
gcloud --quiet config set compute/zone ${ZONE}
gcloud --quiet container clusters get-credentials $CLUSTER

gcloud docker -- push gcr.io/${PROJECT_ID}/${PINGOUT_IMAGE}

yes | gcloud beta container images add-tag gcr.io/${PROJECT_ID}/${PINGOUT_IMAGE}:$TRAVIS_COMMIT gcr.io/${PROJECT_ID}/${PINGOUT_IMAGE}:latest

kubectl set image deployment/${PINGOUT_DEPLOYMENT} ${PINGOUT_CONTAINER}=gcr.io/${PROJECT_ID}/${PINGOUT_IMAGE}:$TRAVIS_COMMIT
