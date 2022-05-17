#!/bin/bash

ENVIRONMENT=TESTNET

TEST_ENVIRONMENT=${ENVIRONMENT} brownie test --network avax-test
