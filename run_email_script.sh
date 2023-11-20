#!/bin/bash

# Function to generate a random sleep time between 10 minutes and 30 minutes
generate_random_sleep() {
  MIN=10
  MAX=30
  echo $(( ( RANDOM % $MAX-$MIN+1 ) + $MIN ))
}

# Generate a random sleep time
sleep_time=$(generate_random_sleep)

# Sleep for the random interval
sleep ${sleep_time}m

# Run the Python script
./venv/bin/python3 ./main.py
