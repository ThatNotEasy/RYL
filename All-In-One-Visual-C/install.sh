#!/bin/bash

echo "Installing all .exe files in the current directory..."

for exe_file in *.exe; do
    echo "Installing $exe_file"
    ./"$exe_file"
done

echo "Installation of .exe files completed."
