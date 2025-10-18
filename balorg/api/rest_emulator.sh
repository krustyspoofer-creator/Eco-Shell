#!/usr/bin/env bash
# balorg/api/rest_emulator.sh
# REST API emulator using curl (Bash version)

API_PORT="${BALORG_API_PORT:-8080}"
LOG_DIR="${BALORG_HOME:-$(dirname "$(dirname "$(readlink -f "$0")"))")}/logs"
mkdir -p "$LOG_DIR"

handle_request() {
    local request="$1"
    local method=$(echo "$request" | grep -oP '^[A-Z]+')
    local path=$(echo "$request" | grep -oP '/[^ ]*')
    local body=$(echo "$request" | sed -n '/^$/,$p' | tail -n +2)
    
    echo "[Balorg API] $method $path"
    
    case "$path" in
        /health)
            echo "HTTP/1.1 200 OK"
            echo "Content-Type: application/json"
            echo ""
            echo '{"status":"healthy","mode":"bash","timestamp":"'$(date +%s)'"}'
            ;;
        /plugins)
            echo "HTTP/1.1 200 OK"
            echo "Content-Type: application/json"
            echo ""
            echo '{"plugins":["example_plugin"],"count":1}'
            ;;
        /execute)
            echo "HTTP/1.1 200 OK"
            echo "Content-Type: application/json"
            echo ""
            echo '{"status":"queued","message":"Plugin execution queued"}'
            ;;
        *)
            echo "HTTP/1.1 404 Not Found"
            echo "Content-Type: application/json"
            echo ""
            echo '{"error":"Not found","path":"'$path'"}'
            ;;
    esac
}

serve_api() {
    echo "[Balorg API] REST emulator running on port $API_PORT"
    echo "[Balorg API] Available endpoints:"
    echo "  GET  /health  - Health check"
    echo "  GET  /plugins - List plugins"
    echo "  POST /execute - Execute plugin"
    
    while true; do
        request=$(nc -l -p "$API_PORT" -q 1)
        handle_request "$request" | nc -l -p "$API_PORT" -q 1 &
    done
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    serve_api
fi
