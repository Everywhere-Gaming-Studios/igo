#!/bin/bash

ENVIRONMENT=MAINNET

echo Starting ${ENVIRONMENT} deployment...
DEPLOY_ENV=${ENVIRONMENT} brownie run deploy_igo_system.py --network avax-main
echo Igo system successfully deployed