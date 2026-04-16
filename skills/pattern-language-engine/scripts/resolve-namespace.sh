#!/usr/bin/env bash
# resolve-namespace.sh
# Reads INDEX.md for mapping instructions like "[G-020 (was G-002):" and resolves buffered .tmp files.

TARGET_DIR=${1:-.}

if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Directory $TARGET_DIR does not exist."
  exit 1
fi

cd "$TARGET_DIR" || exit 1

if [ ! -f "INDEX.md" ]; then
  echo "Error: INDEX.md not found in $TARGET_DIR."
  exit 1
fi

echo "Analyzing INDEX.md for re-mappings..."

# Extract mappings: Format is "[NEW_ID (was OLD_ID):"
mappings=$(grep -oE '\[[A-Za-z0-9-]+ \(was [A-Za-z0-9-]+\):' INDEX.md | sed -E 's/\[([A-Za-z0-9-]+) \(was ([A-Za-z0-9-]+)\):/\1 \2/')

if [ -z "$mappings" ]; then
  echo "No mappings found in INDEX.md. Ensure format is '[NEW_ID (was OLD_ID):'."
  exit 1
fi

# Arrays to keep track of new and old IDs
new_ids=()
old_ids=()

while read -r new_id old_id; do
  new_ids+=("$new_id")
  old_ids+=("$old_id")
done <<< "$mappings"

# Validate (b) no duplicate new IDs
duplicate=$(printf "%s\n" "${new_ids[@]}" | sort | uniq -d)
if [ -n "$duplicate" ]; then
  echo "Validation Error: Duplicate new IDs found in INDEX.md: $duplicate"
  exit 1
fi

# Validate (a) correct mapping to tmp files
errors=0
for i in "${!old_ids[@]}"; do
  old="${old_ids[$i]}"
  new="${new_ids[$i]}"
  
  # Find the matching tmp file. E.g., G-002-wisdom.md.tmp
  # We use an array to catch multiple matches or zero matches
  matches=( "$old"-*.md.tmp )
  
  if [ ! -e "${matches[0]}" ]; then
    echo "Error: No .tmp file found for old ID: $old"
    errors=$((errors + 1))
  elif [ ${#matches[@]} -gt 1 ]; then
    echo "Error: Multiple .tmp files found for old ID: $old"
    errors=$((errors + 1))
  fi
done

if [ $errors -gt 0 ]; then
  echo "Validation failed. Sequence mismatch detected. Aborting resolve."
  exit 1
fi

echo "Validation passed. Executing renames in one shot..."

for i in "${!old_ids[@]}"; do
  old="${old_ids[$i]}"
  new="${new_ids[$i]}"
  
  # file expands to the actual file path because we validated its existence above
  for actual_file in "$old"-*.md.tmp; do
    # Replace old ID with new ID in filename, and remove .tmp
    base_name=$(basename "$actual_file" .tmp)
    new_name="${base_name/$old/$new}"
    
    mv "$actual_file" "$new_name"
    echo "Resolved: $actual_file -> $new_name"
  done
done

# Determine if any tmp files were left behind
lingering=$(ls -1 *-*.md.tmp 2>/dev/null | wc -l)
if [ "$lingering" -gt 0 ]; then
  echo "Warning: $lingering .tmp files were NOT resolved because they were missing from the INDEX.md mapping."
else
  echo "Success: All mapped files resolved perfectly. No .tmp files remaining."
fi
