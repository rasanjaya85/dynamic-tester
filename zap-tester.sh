#!/usr/bin/env bash

TARGET_VERSION=$1

# the target URL for ZAP to scan
TARGET_URL="http://192.168.33.20:8888"

printf "Starting the Product Container"
PRODUCT_CONTAINER_ID=$(docker run -p 8888:8080 -d registry.wso2.org/weather-service:1.0.${TARGET_VERSION})

if [ $? -eq 0 ]; then
    printf "Starting the Zap Container"
    ZAP_CONTAINER_ID=$(docker run -u zap -p 2375:2375 -d owasp/zap2docker-weekly zap.sh -daemon -port 2375 -host 127.0.0.1 -config api.disablekey=true -config scanner.attackOnStart=true -config view.mode=attack)
else
    exit
fi

docker exec $ZAP_CONTAINER_ID zap-cli -p 2375 status -t 60 && docker exec $ZAP_CONTAINER_ID zap-cli -p 2375 open-url $TARGET_URL
docker exec $ZAP_CONTAINER_ID zap-cli -p 2375 spider $TARGET_URL
docker exec $ZAP_CONTAINER_ID zap-cli -p 2375 active-scan -r $TARGET_URL
docker exec $ZAP_CONTAINER_ID zap-cli -p 2375 alerts

# docker logs [container ID or name]
divider==================================================================
printf "\n"
printf "$divider"
printf "ZAP-daemon log output follows"
printf "$divider"
printf "\n"

docker exec $ZAP_CONTAINER_ID zap-cli -p 2375 report -o vulnerability.html -f html

#docker logs $ZAP_CONTAINER_ID
docker stop $ZAP_CONTAINER_ID $PRODUCT_CONTAINER_ID && docker rm $ZAP_CONTAINER_ID $PRODUCT_CONTAINER_ID