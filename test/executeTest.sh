#!/bin/bash

python3 ../ClientTest.py -e ./test01 &
for ((i=1; i<=100; i++))
do
    python3 ../ClientTest.py -d ./test01 &
done