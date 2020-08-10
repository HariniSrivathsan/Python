#!/usr/bin/env bash

printf "\n"
echo "**** Ingesting Inspection File ****"
echo `python3 main.py inspection`

echo "\n"
echo "**** Ingesting License Start File ****"
echo `python3 main.py license_start`

echo "\n"
echo "**** Ingesting License End File ****"
echo `python3 main.py license_end`

