#!/bin/bash
coverage erase
for i in test/*_test.py; do
    PYTHONPATH=src/ coverage run --branch --source=src/ -a $i; 
done
coverage html
