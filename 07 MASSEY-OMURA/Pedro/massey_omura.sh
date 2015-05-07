#!/bin/bash

echo "Cripto con chiave Ka"
python massey_omura.py Lena.tga Lena_A.tga -e key.bin

echo "Cripto con chiave Kb"
python massey_omura.py Lena_A.tga Lena_AB.tga -e key2.bin

echo "Decripto con chiave Ka"
python massey_omura.py Lena_AB.tga Lena_B.tga -d key.bin

echo "Decripto con chiave Kb"
python massey_omura.py Lena_B.tga Lena_decrypt.tga -d key2.bin
