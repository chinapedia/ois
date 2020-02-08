# apt install curl jq

curl -s https://api.github.com | jq --raw-output ".notifications_url" | tail -c 2
