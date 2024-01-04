#!/bin/bash

# Define the file path
file="/etc/passwd"

# Check if the hash file exists
if [ -f "passwd_hash.txt" ]; then
  # Read the last saved hash from the file
  last_hash=$(cat passwd_hash.txt)
else
  # If the hash file doesn't exist, create it with the current hash
  last_hash=$(sha1sum $file | cut -d ' ' -f 1)
  echo $last_hash > passwd_hash.txt
fi

# Calculate the current hash
current_hash=$(sha1sum $file | cut -d ' ' -f 1)

# Compare the current hash with the last saved hash
if [ "$current_hash" = "$last_hash" ]; then
  echo "Hashes match. No changes detected."
else
  echo "Hashes do not match. Changes detected."
  # Update the hash file with the new hash
  echo $current_hash > passwd_hash.txt
fi
