#!/bin/bash

rm -f *.o analyzer

make

./analyzer general.conf.txt
