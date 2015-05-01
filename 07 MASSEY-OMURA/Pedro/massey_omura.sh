#!/bin/bash

python massey_omura.py Lena.jpg Lena_EA.jpg -e key.bin

python massey_omura.py Lena_EA.jpg Lena_EA_EB.jpg -e key2.bin

python massey_omura.py Lena_EA_EB.jpg Lena_EB.jpg -d key.bin

python massey_omura.py Lena_EB.jpg Lena_decrypt.jpg -d key2.bin
