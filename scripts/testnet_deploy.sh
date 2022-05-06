#!/bin/bash

ENVIRONMENT=TESTNET

echo Starting ${ENVIRONMENT} deployment...
DEPLOY_ENV=${ENVIRONMENT} brownie run deploy_igo_system.py --network avax-test
echo Igo system successfully deployed