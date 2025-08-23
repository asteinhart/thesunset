#!/bin/bash

# create new screen
screen -S sunset

# cd to the sunset directory
cd /thesunset/detector

# start env
source sunset/bin/activate

# run the main script
python3 scheduler.py