#!/bin/bash

str1="...."
str2="..TR"
str3="LE.."

while read line; do
	last4="${line: -4}"
	#echo $last4
	if [ "$last4" == "$str1" ]; then
        echo $line >> pulito.txt
    fi
    if [ "$last4" == "$str2" ]; then
        echo $line >> pulito.txt
    fi
    if [ "$last4" == "$str3" ]; then
        echo $line >> pulito.txt
    fi
done < tcflow.txt

echo "`cat pulito.txt | cut -d':' -f 2`\n"  > pulito.txt

while read line; do
    for word in $line; do
        if test ${#word} -eq ${#str1}; then
        	echo $word >> superpulito.txt
        fi
    done
done < pulito.txt

#superpulito.txt file con soli dati