#!/bin/bash

echo "1"
python massey_omura.py Lena.tga Lena_A.tga -e key.bin

echo "2"
python massey_omura.py Lena_A.tga Lena_AB.tga -e key2.bin

echo "3"
python massey_omura.py Lena_AB.tga Lena_B.tga -d key.bin

echo "4"
python massey_omura.py Lena_B.tga Lena_decrypt.tga -d key2.bin
