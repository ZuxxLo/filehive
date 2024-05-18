#!/bin/sh


FLAG_FILE=/app/flag


if [ ! -e "$FLAG_FILE" ]; then
    touch "$FLAG_FILE"
    echo "********EXECUTING ENTRYPOINT********"
    bash /app/entrypoint.sh
 
else
    bash /app/start.sh
fi