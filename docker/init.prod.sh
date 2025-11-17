#!/bin/bash

if [ ! -d "/src/app/log" ]; then
    mkdir /src/app/log
    if [ ! -f "/src/app/log/app.log"]; then
        cat /dev/null > /src/app/log/app.log
    fi
fi

gunicorn --bind 0.0.0.0:5000 app:app