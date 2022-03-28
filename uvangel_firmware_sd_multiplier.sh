#!/bin/bash

OPENAIR_HOURS=470
FIRST_COMMIT=21373f562f2bde292a37c82bdc0484e5420abf06
LAST_COMMIT=ffe48f6bfb80f51702d6e01ae1693e54b7213e1a
REPO_PATH=$HOME/src/uvangel_firmware
IGNORE_DIR="(build|data|third-party|html|node_modules|proto-c|wasm_runner\/examples|emsdk|docs\/assets)"
IGNORE_FILE="(package-lock.json)"

./sd_multiplier.sh  \
    $REPO_PATH \
    $OPENAIR_HOURS \
    $FIRST_COMMIT \
    $LAST_COMMIT \
    $IGNORE_DIR \
    $IGNORE_FILE
