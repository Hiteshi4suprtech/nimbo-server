#!/bin/bash

# Check if the file exists before deploying
if [ -f /home/ubuntu/nimbo-server/.gitignore ]; then
    echo ".gitignore already exists. Skipping."
else
    cp /path/to/source/.gitignore /home/ubuntu/nimbo-server/
fi

# Other deployment steps...
