#!/bin/bash
cd "$(dirname "$0")"

sites=("https://www.google.com" "https://www.github.com" "https://www.google.com/blablabla")

for site in "${sites[@]}"; do
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    result=$(curl -L -o /dev/null -s -w "%{http_code} %{time_total}" "$site")
    read -r code time <<< "$result"

    if [ "$code" -ge 200 ] && [ "$code" -lt 400 ]; then
        status="UP"
    else
        status="DOWN"
    fi

    echo "$timestamp $status $code $time $site" >> results.log
done



