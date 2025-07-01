#!/bin/sh

echo "Please select the window about which you would like to stream."
WINDOW_ID=$(xwininfo | rg 'xwininfo: Window id: (\w+)( .+)' -r '$1')
env WINDOW_ID="$WINDOW_ID" uv run m5rs
