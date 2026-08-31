#!/bin/zsh

set -euo pipefail

readonly PROJECT_CONFIG_NAME=".ios-install-skill.json"
readonly LOCAL_CONFIG_NAME=".ios-install-skill.local.json"
readonly SCRIPT_NAME="${0:t}"
readonly SCRIPT_DIRECTORY="${0:A:h}"
readonly JSON_HELPER="$SCRIPT_DIRECTORY/ios-install-json.py"
readonly DEVICE_PROBE_TIMEOUT_SECONDS=10
readonly DEVICE_RELIST_ATTEMPTS=3
readonly DEVICE_RELIST_DELAY_SECONDS=1

fail() {
  print -u2 -- "error: $*"
  exit 1
}

usage() {
  print -- "Usage: $SCRIPT_NAME [--resolve-only] [--save-device-selection] [repository-root]"
}

resolve_only=0
save_device_selection=0
while (( $# > 0 )); do
  case "$1" in
    --resolve-only)
      resolve_only=1
      shift
      ;;
    --save-device-selection)
      save_device_selection=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      fail "Unknown option: $1"
      ;;
    *)
      break
      ;;
  esac
done
(( $# <= 1 )) || fail "Expected at most one repository-root argument."

repository_root="${1:-$PWD}"
[[ -d "$repository_root" ]] || fail "Repository directory does not exist: $repository_root"
repository_root="${repository_root:A}"
cd "$repository_root"

project_config="$repository_root/$PROJECT_CONFIG_NAME"
local_config="$repository_root/$LOCAL_CONFIG_NAME"

validate_config() {
  local kind="$1"
  local config_path="$2"
  [[ -f "$config_path" ]] || return 0
  python3 "$JSON_HELPER" validate-config "$kind" "$config_path"
}

config_value() {
  local key="$1"
  local value

  if [[ -f "$local_config" ]]; then
    value=$(plutil -extract "$key" raw -o - -- "$local_config" 2>/dev/null || true)
    if [[ -n "$value" ]]; then
      print -r -- "$value"
      return 0
    fi
  fi

  if [[ -f "$project_config" ]]; then
    value=$(plutil -extract "$key" raw -o - -- "$project_config" 2>/dev/null || true)
    if [[ -n "$value" ]]; then
      print -r -- "$value"
      return 0
    fi
  fi
}

[[ -f "$JSON_HELPER" ]] || fail "Missing JSON resolver: $JSON_HELPER"
command -v python3 >/dev/null 2>&1 || fail "python3 is required to parse Xcode and CoreDevice JSON."
validate_config project "$project_config"
validate_config local "$local_config"

case "${IOS_GENERATE_PROJECT:-0}" in
  0)
    ;;
  1)
    [[ -f project.yml ]] || fail "IOS_GENERATE_PROJECT=1 but project.yml does not exist."
    command -v xcodegen >/dev/null 2>&1 || fail "IOS_GENERATE_PROJECT=1 but xcodegen is not installed."
    print -- "Generating Xcode project from project.yml..."
    xcodegen generate
    ;;
  *)
    fail "IOS_GENERATE_PROJECT must be 0 or 1."
    ;;
esac

[[ -z "${IOS_PROJECT:-}" || -z "${IOS_WORKSPACE:-}" ]] || fail "Set only one of IOS_PROJECT or IOS_WORKSPACE."

container_source="discovery"
if [[ -n "${IOS_PROJECT:-}" ]]; then
  build_container="$IOS_PROJECT"
  build_selector=(-project "$build_container")
  container_kind="project"
  container_source="IOS_PROJECT"
elif [[ -n "${IOS_WORKSPACE:-}" ]]; then
  build_container="$IOS_WORKSPACE"
  build_selector=(-workspace "$build_container")
  container_kind="workspace"
  container_source="IOS_WORKSPACE"
else
  configured_container=$(config_value container || true)
  if [[ -n "$configured_container" ]]; then
    build_container="$configured_container"
    container_source="configuration"
    case "$build_container" in
      *.xcworkspace)
        build_selector=(-workspace "$build_container")
        container_kind="workspace"
        ;;
      *.xcodeproj)
        build_selector=(-project "$build_container")
        container_kind="project"
        ;;
      *)
        fail "Configured container must end in .xcworkspace or .xcodeproj: $build_container"
        ;;
    esac
  else
    workspaces=( *.xcworkspace(N) )
    projects=( *.xcodeproj(N) )

    if (( ${#workspaces[@]} == 1 )); then
      build_container="$workspaces[1]"
      build_selector=(-workspace "$build_container")
      container_kind="workspace"
    elif (( ${#workspaces[@]} > 1 )); then
      print -u2 -- "Multiple workspaces found: ${workspaces[*]}"
      fail "Set IOS_WORKSPACE or configure container in $PROJECT_CONFIG_NAME."
    elif (( ${#projects[@]} == 1 )); then
      build_container="$projects[1]"
      build_selector=(-project "$build_container")
      container_kind="project"
    elif (( ${#projects[@]} == 0 )); then
      fail "No top-level .xcworkspace or .xcodeproj found. Generate the project explicitly if needed."
    else
      print -u2 -- "Multiple projects found: ${projects[*]}"
      fail "Set IOS_PROJECT or configure container in $PROJECT_CONFIG_NAME."
    fi
  fi
fi
[[ -d "$build_container" ]] || fail "Build container does not exist: $build_container"

scheme_source="discovery"
scheme="${IOS_SCHEME:-}"
if [[ -n "$scheme" ]]; then
  scheme_source="IOS_SCHEME"
else
  scheme=$(config_value scheme || true)
  [[ -z "$scheme" ]] || scheme_source="configuration"
fi

scheme_has_ios_application() {
  local candidate="$1"
  local settings
  settings=$(xcodebuild "${build_selector[@]}" \
    -scheme "$candidate" \
    -sdk iphoneos \
    -destination "generic/platform=iOS" \
    -showBuildSettings \
    -json) || return 2
  print -rn -- "$settings" | python3 "$JSON_HELPER" has-ios-application
}

if [[ -z "$scheme" ]]; then
  scheme_listing=$(xcodebuild "${build_selector[@]}" -list -json)
  schemes=("${(@f)$(print -rn -- "$scheme_listing" | python3 "$JSON_HELPER" schemes "$container_kind")}")
  schemes=(${schemes:#})
  ios_application_schemes=()
  for candidate in "${schemes[@]}"; do
    if scheme_has_ios_application "$candidate"; then
      ios_application_schemes+=("$candidate")
    else
      scheme_status=$?
      (( scheme_status == 1 )) || fail "Xcode could not inspect scheme: $candidate"
    fi
  done

  if (( ${#ios_application_schemes[@]} == 1 )); then
    scheme="$ios_application_schemes[1]"
  elif (( ${#ios_application_schemes[@]} == 0 )); then
    fail "No scheme producing an iOS application was discovered. Set IOS_SCHEME or configure scheme in $PROJECT_CONFIG_NAME."
  else
    print -u2 -- "Multiple iOS application schemes found: ${ios_application_schemes[*]}"
    fail "Set IOS_SCHEME or configure scheme in $PROJECT_CONFIG_NAME."
  fi
else
  if scheme_has_ios_application "$scheme"; then
    :
  else
    scheme_status=$?
    (( scheme_status == 1 )) && fail "Scheme does not resolve to an iOS application: $scheme"
    fail "Xcode could not inspect scheme: $scheme"
  fi
fi

configuration="${IOS_CONFIGURATION:-}"
configuration_source="IOS_CONFIGURATION"
if [[ -z "$configuration" ]]; then
  configuration=$(config_value configuration || true)
  configuration_source="configuration"
fi
if [[ -z "$configuration" ]]; then
  configuration="Debug"
  configuration_source="default"
fi

device_name="${IOS_DEVICE_NAME:-}"
device_identifier="${IOS_DEVICE_IDENTIFIER:-}"
device_hint="${IOS_DEVICE_HINT:-}"
device_selector_count=0
[[ -z "$device_name" ]] || (( device_selector_count += 1 ))
[[ -z "$device_identifier" ]] || (( device_selector_count += 1 ))
[[ -z "$device_hint" ]] || (( device_selector_count += 1 ))
(( device_selector_count <= 1 )) || fail "Set only one of IOS_DEVICE_NAME, IOS_DEVICE_IDENTIFIER, or IOS_DEVICE_HINT."
device_selection_source=""
if [[ -n "$device_name" ]]; then
  device_selection_source="IOS_DEVICE_NAME"
elif [[ -n "$device_identifier" ]]; then
  device_selection_source="IOS_DEVICE_IDENTIFIER"
elif [[ -n "$device_hint" ]]; then
  device_selection_source="IOS_DEVICE_HINT"
fi
if [[ -z "$device_name" && -z "$device_identifier" && -z "$device_hint" ]]; then
  if [[ -f "$local_config" ]]; then
    device_identifier=$(plutil -extract deviceIdentifier raw -o - -- "$local_config" 2>/dev/null || true)
    if [[ -n "$device_identifier" ]]; then
      device_selection_source="$LOCAL_CONFIG_NAME"
    else
      device_name=$(plutil -extract deviceName raw -o - -- "$local_config" 2>/dev/null || true)
      if [[ -n "$device_name" ]]; then
        device_selection_source="$LOCAL_CONFIG_NAME legacy deviceName"
      fi
    fi
  fi
fi

if (( save_device_selection == 1 )) && [[ "$device_selection_source" != "IOS_DEVICE_NAME" ]]; then
  fail "--save-device-selection requires a human-readable IOS_DEVICE_NAME selection."
fi

list_core_devices() {
  xcrun devicectl list devices \
    --json-output - \
    --omit-deprecated-fields-in-json \
    --quiet
}

apply_device_resolution() {
  local preserve_selection_reason="${2:-0}"
  device_resolution="$1"
  device_identifier=$(print -rn -- "$device_resolution" | plutil -extract identifier raw -o - -- -)
  device_name=$(print -rn -- "$device_resolution" | plutil -extract name raw -o - -- -)
  device_connection_description=$(
    print -rn -- "$device_resolution" | python3 "$JSON_HELPER" describe-connection
  )
  if (( preserve_selection_reason == 0 )); then
    device_selection_reason=$(
      print -rn -- "$device_resolution" | plutil -extract selectionReason raw -o - -- -
    )
  fi
}

refresh_selected_device() {
  local refreshed_listing
  local refreshed_resolution

  refreshed_listing=$(list_core_devices) || return 1
  refreshed_resolution=$(
    print -rn -- "$refreshed_listing" \
      | python3 "$JSON_HELPER" resolve-device --identifier "$device_identifier"
  ) || return 1
  apply_device_resolution "$refreshed_resolution" 1
}

ensure_device_connected() {
  local next_stage="$1"
  local refresh_first="${2:-1}"
  local attempt

  if (( refresh_first == 1 )); then
    refresh_selected_device \
      || fail "CoreDevice could not refresh $device_name before $next_stage."
  fi

  if print -rn -- "$device_resolution" | python3 "$JSON_HELPER" is-connected; then
    print -- "Device ready before $next_stage: $device_name is $device_connection_description."
    return 0
  fi

  if ! print -rn -- "$device_resolution" | python3 "$JSON_HELPER" can-activate-wirelessly; then
    fail "$device_name is $device_connection_description and cannot continue to $next_stage. Connect or pair the device, then retry."
  fi

  print -- "Activating paired wireless device $device_name before $next_stage..."
  if ! xcrun devicectl device info details \
    --device "$device_identifier" \
    --timeout "$DEVICE_PROBE_TIMEOUT_SECONDS" \
    --quiet >/dev/null; then
    fail "$device_name is paired wireless but activation failed before $next_stage within ${DEVICE_PROBE_TIMEOUT_SECONDS}s. Confirm the phone is unlocked, on the same local network, and available to Xcode."
  fi

  for (( attempt = 1; attempt <= DEVICE_RELIST_ATTEMPTS; attempt++ )); do
    (( attempt == 1 )) || sleep "$DEVICE_RELIST_DELAY_SECONDS"
    if refresh_selected_device \
      && print -rn -- "$device_resolution" | python3 "$JSON_HELPER" is-connected; then
      print -- "Device ready before $next_stage: $device_name is $device_connection_description."
      return 0
    fi
  done

  fail "$device_name remained $device_connection_description after wireless activation before $next_stage. Confirm the phone is unlocked, on the same local network, and available to Xcode."
}

if ! device_listing=$(list_core_devices); then
  fail "CoreDevice could not enumerate physical iOS devices."
fi
device_arguments=()
[[ -z "$device_name" ]] || device_arguments+=(--name "$device_name")
[[ -z "$device_identifier" ]] || device_arguments+=(--identifier "$device_identifier")
[[ -z "$device_hint" ]] || device_arguments+=(--hint "$device_hint")
if ! device_resolution=$(print -rn -- "$device_listing" | python3 "$JSON_HELPER" resolve-device "${device_arguments[@]}"); then
  print -rn -- "$device_listing" | python3 "$JSON_HELPER" list-devices
  fail "CoreDevice could not choose a usable physical iOS device."
fi
apply_device_resolution "$device_resolution"
print -- "Selected device: $device_name ($device_identifier)"
print -- "Selection reason: $device_selection_reason"
ensure_device_connected "build" 0

save_resolved_device() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && ! git check-ignore -q -- "$LOCAL_CONFIG_NAME"; then
    fail "Refusing to save a device identifier until $LOCAL_CONFIG_NAME is ignored by Git."
  fi
  python3 "$JSON_HELPER" save-device-config "$local_config" "$device_identifier"
  print -- "Saved $device_name as $device_identifier in $LOCAL_CONFIG_NAME."
}

if (( save_device_selection == 1 )); then
  save_resolved_device
elif [[ "$device_selection_source" == "$LOCAL_CONFIG_NAME legacy deviceName" ]]; then
  save_resolved_device
  print -- "Migrated the legacy saved device name to its stable identifier."
fi

derived_data_arguments=()
if [[ -n "${IOS_DERIVED_DATA_PATH:-}" ]]; then
  derived_data_arguments=(-derivedDataPath "$IOS_DERIVED_DATA_PATH")
  derived_data_description="$IOS_DERIVED_DATA_PATH"
else
  derived_data_description="Xcode default"
fi

print -- "Resolved iOS installation:"
print -- "  Repository: $repository_root"
print -- "  Container: $build_container ($container_source)"
print -- "  Scheme: $scheme ($scheme_source)"
print -- "  Configuration: $configuration ($configuration_source)"
print -- "  Device: $device_name ($device_identifier)"
print -- "  Connection: $device_connection_description"
print -- "  DerivedData: $derived_data_description"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  print -- "  Git branch: $(git branch --show-current)"
  print -- "  Git commit: $(git rev-parse --short HEAD)"
  dirty_files=$(git status --short)
  if [[ -n "$dirty_files" ]]; then
    print -- "  Working tree changes:"
    while IFS= read -r dirty_file; do
      print -- "    $dirty_file"
    done <<< "$dirty_files"
  else
    print -- "  Working tree: clean"
  fi
fi

(( resolve_only == 0 )) || exit 0

print -- "Building $scheme ($configuration) for $device_name..."
xcodebuild build "${build_selector[@]}" \
  -scheme "$scheme" \
  -configuration "$configuration" \
  -destination "id=$device_identifier" \
  "${derived_data_arguments[@]}" \
  -allowProvisioningUpdates

build_settings=$(xcodebuild "${build_selector[@]}" \
  -scheme "$scheme" \
  -configuration "$configuration" \
  -destination "id=$device_identifier" \
  "${derived_data_arguments[@]}" \
  -showBuildSettings \
  -json)
app_product=$(print -rn -- "$build_settings" | python3 "$JSON_HELPER" app-product)
target_build_directory=$(print -rn -- "$app_product" | plutil -extract targetBuildDirectory raw -o - -- -)
wrapper_name=$(print -rn -- "$app_product" | plutil -extract wrapperName raw -o - -- -)
app_path="$target_build_directory/$wrapper_name"
[[ -d "$app_path" ]] || fail "Resolved app bundle does not exist: $app_path"
bundle_identifier=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$app_path/Info.plist") || fail "Could not read the built app's bundle identifier."

ensure_device_connected "install"
print -- "Installing $bundle_identifier on $device_name..."
xcrun devicectl device install app --device "$device_identifier" "$app_path"

ensure_device_connected "launch"
print -- "Launching $bundle_identifier on $device_name..."
xcrun devicectl device process launch --device "$device_identifier" "$bundle_identifier"

print -- "Installed and launched $bundle_identifier on $device_name."
