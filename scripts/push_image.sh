#!/bin/bash


image=$1
docker tag $image myhome.com:5000/$image
docker push myhome.com:5000/$image
