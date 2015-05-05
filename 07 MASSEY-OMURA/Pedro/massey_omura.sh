#!/bin/bash

echo "1"
python massey_omura.py ipnorospo.tga ipnorospo_EA.tga -e key.bin

echo "2"
python massey_omura.py ipnorospo_EA.tga ipnorospo_EA_EB.tga -e key2.bin

echo "3"
python massey_omura.py ipnorospo_EA_EB.tga ipnorospo_EB.tga -d key.bin

echo "4"
python massey_omura.py ipnorospo_EB.tga ipnorospo_decrypt.tga -d key2.bin
