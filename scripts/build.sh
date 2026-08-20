#!/bin/bash

# Prepare for build
BUILD_FOLDER=("build")
BUILD_DEPS=("python" "dotnet-sdk-10.0" "python3-tk")
apt install "${BUID_DEPS}" || sudo apt install "${BUID_DEPS}"

# Verify and preapre build environment
[[ $(basename $(pwd)) == "MC-Sky-Builder" ]] && ( echo "Please run the script in the root path of this project!"; exit 1)
[[ -d "${BUILD_FOLDER}" ]] || mkdir "${BUILD_FOLDER}"

# Compile external libs
dotnet build generator

# Compile Main Program
source src/.venv/bin/activate
pip install -r requirements.txt
