#!/bin/bash

host="db"
port="5432"

echo "Waiting db on ${host}:${port}..."

while !</dev/tcp/${host}/${port};
do
  sleep 1; 
done;

echo "db is running"