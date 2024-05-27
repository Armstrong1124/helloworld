#!/bin/bash

target_directory="./src/tool/"

# Define clang-format path
CLANG_FORMAT="clang-format"

# Format files in the target directory
if [ -d "$target_directory" ]; then
    echo "Formatting directory: $target_directory"
    find "$target_directory" -type d \( -name 'alg_lib' -prune \) -o \( -type f \( -name '*.cc' -o -name '*.h' \) -exec $CLANG_FORMAT -i {} \; \)
else
    echo "Directory $target_directory does not exist."
fi
