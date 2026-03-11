#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Extract data
model=$(echo "$input" | jq -r '.model.display_name')
usage=$(echo "$input" | jq '.context_window.current_usage')
context_window_size=$(echo "$input" | jq -r '.context_window.context_window_size')

# ANSI color codes
CYAN='\033[36m'
YELLOW='\033[33m'
GREEN='\033[32m'
MAGENTA='\033[35m'
RESET='\033[0m'

# Build status line
printf "${CYAN}%s${RESET}" "$model"

# Calculate context usage if available
if [ "$usage" != "null" ]; then
    current_tokens=$(echo "$usage" | jq '.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens')
    output_tokens=$(echo "$usage" | jq '.output_tokens')
    
    # Calculate percentage
    percentage=$((current_tokens * 100 / context_window_size))
    
    printf " ${YELLOW}│${RESET}"
    printf " ${GREEN}Context: %d/%dk (%d%%)${RESET}" "$current_tokens" "$((context_window_size / 1000))" "$percentage"
    printf " ${YELLOW}│${RESET}"
    printf " ${MAGENTA}Output: %dk${RESET}" "$((output_tokens / 1000))"
else
    printf " ${YELLOW}│${RESET}"
    printf " ${GREEN}Context: 0/%dk (0%%)${RESET}" "$((context_window_size / 1000))"
fi
