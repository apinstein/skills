#!/usr/bin/env bash
# buffer-namespace.sh
# Renames all pattern files (e.g. G-001-*.md) to .tmp to safely clear the ID namespace before a re-indexing sweep.

TARGET_DIR=${1:-.}

if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Directory $TARGET_DIR does not exist."
  exit 1
fi

cd "$TARGET_DIR" || exit 1

count=0
for f in *-*.md; do
  # Skip if no matches
  [ -e "$f" ] || continue
  
  mv "$f" "$f.tmp"
  count=$((count + 1))
done

echo "Buffered $count pattern files to .tmp in $TARGET_DIR"
