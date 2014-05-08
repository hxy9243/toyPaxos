#!/bin/bash

for i in {1..2}
do

python prop.py _config2 ${i} &

done
