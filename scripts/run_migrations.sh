#!/bin/bash
APP_EXEC="python3 manage.py"

flag=0
retries=0
while [ $flag -eq 0 ]; do
    if [ $retries -eq 10 ]; then
        echo Executed $retries retries, aborting
        exit 1
    fi

    $APP_EXEC inspectdb > /dev/null

    if [ $? -eq 0 ]; then
        flag=1
    else
        echo "Database migration failed, retrying in 5 seconds..."
        sleep 5
        let retries++
    fi
done

$APP_EXEC migrate --noinput
echo "Database migrated."
