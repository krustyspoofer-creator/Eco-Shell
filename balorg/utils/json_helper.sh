#!/usr/bin/env bash
# balorg/utils/json_helper.sh
# JSON processing utilities using jq

json_get() {
    local json_data="$1"
    local key_path="$2"
    echo "$json_data" | jq -r "$key_path"
}

json_set() {
    local json_data="$1"
    local key_path="$2"
    local value="$3"
    echo "$json_data" | jq --arg val "$value" "$key_path = \$val"
}

json_validate() {
    local json_data="$1"
    echo "$json_data" | jq empty 2>/dev/null
    return $?
}

json_pretty() {
    local json_data="$1"
    echo "$json_data" | jq '.'
}

# Export functions
export -f json_get
export -f json_set
export -f json_validate
export -f json_pretty
