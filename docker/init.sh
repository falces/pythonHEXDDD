#!/bin/bash

cat /dev/null > /src/app/log/app.log
flask run --host=0.0.0.0 --debug