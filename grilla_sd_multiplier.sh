#!/bin/bash

OPENAIR_HOURS=1051
FIRST_COMMIT=360ff579b0dea79d22a119cadd13ae07e36dd797
LAST_COMMIT=1cf803e0b211ffa7d1872f8cff61a4cdd0b29e3e
REPO_PATH=$HOME/src/grilla-embedded
IGNORE_DIR="(build|data|third-party|html|proto-c|docs\/assets|main\/legacy)"
IGNORE_FILE="(package-lock.json)"

./sd_multiplier.sh  \
    $REPO_PATH \
    $OPENAIR_HOURS \
    $FIRST_COMMIT \
    $LAST_COMMIT \
    $IGNORE_DIR \
    $IGNORE_FILE \
