#!/bin/bash
set -x

cd /tmp
python3 /lbn/inventory.py
cat inventory.json
python3 /lbn/push_on_s3.py
