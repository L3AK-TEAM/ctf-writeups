#!/bin/bash

curl "http://mercury.picoctf.net:15931/index.php" -I HEAD -s | grep pico | cut -d ":" -f 2
