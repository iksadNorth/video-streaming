#!/bin/bash


image=$1
docker tag $image myhome:5000/$image
docker push myhome:5000/$image
