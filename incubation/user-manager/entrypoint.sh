#!/bin/sh

# Write environment variables to /app/.env
printenv > /app/.env

# Execute the main container CMD
exec "$@"
