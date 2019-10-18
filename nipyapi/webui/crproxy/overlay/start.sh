#!/bin/bash

gcloud container clusters get-credentials ${CLUSTER} --region ${REGION}
kubectl port-forward --address 0.0.0.0 svc/nifi ${PORT}:8080
