#!/bin/bash

echo "1"
python massey_omura.py Lena.tga Lena_EA.tga -e key.bin

echo "2"
python massey_omura.py Lena_EA.tga Lena_EA_EB.tga -e key2.bin

echo "3"
python massey_omura.py Lena_EA_EB.tga Lena_EB.tga -d key.bin

echo "4"
python massey_omura.py Lena_EB.tga Lena_decrypt.tga -d key2.bin
