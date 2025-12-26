#!/bin/bash

if [ ! -d "/src/app/log" ]; then
    mkdir /src/app/log
    if [! -f "/src/app/log/app.log"]; then
        cat /dev/null > /src/app/log/app.log
    fi
fi

flask db upgrade

flask run --host=0.0.0.0 --debug