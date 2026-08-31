---
name: install-ios-on-phone
description: Build, code-sign, install, and launch the current iOS app on a connected physical device. Use when the user asks to install, deploy, build and run, or put the current iOS project on their phone or iPad.
---

# Install iOS on Phone

Deploy the current repository's iOS application to a connected physical iOS
device. Resolve the project, scheme, configuration, and device from explicit
overrides, project-root configuration, or Xcode/CoreDevice discovery. Never
guess between viable application schemes. For registered development devices,
make and report a best-effort device choice instead of asking for confirmation.

## Workflow

1. Work from the intended repository or worktree. Report its branch, commit,
   and material uncommitted files before installing.
2. Resolve the skill directory relative to this `SKILL.md`, then enumerate the
   known physical iOS devices before choosing one:

   ```zsh
   <skill-directory>/scripts/install-current-ios-app.sh --list-devices "$PWD"
   ```

3. Choose the device yourself from that structured list using the user's words
   and the conversation's context. Treat wording such as “phone” versus
   “iPhone” semantically; do not pass an approximate label to a deterministic
   helper. Consider device kind and name first, then connection readiness,
   pairing/transport state, and recent CoreDevice activity. Prefer a currently
   connected matching phone over a similarly named disconnected development
   phone. Do not ask for confirmation merely because multiple registered
   development devices are listed. When there is a plausible best choice, tell
   the user which device you chose and why, then pass its exact stable identifier
   to the installer:

   ```zsh
   IOS_DEVICE_IDENTIFIER="<identifier-from-device-list>" \
     <skill-directory>/scripts/install-current-ios-app.sh "$PWD"
   ```

   Honor an explicit stable identifier or a valid saved local identifier unless
   the current request points to another device. Ask only when no candidate is a
   plausible match or choosing one would contradict the user's explicit request.

   Use an exact human-readable name only when the user explicitly chooses it. To
   persist that exact choice, save only the resulting stable identifier:

   ```zsh
   IOS_DEVICE_NAME="My iPhone" \
     <skill-directory>/scripts/install-current-ios-app.sh \
     --save-device-selection "$PWD"
   ```

   Ensure `.ios-install-skill.local.json` is ignored by Git before saving it.
   If a saved identifier no longer matches a known device, report the mismatch.
   Do not silently override an explicit or saved stable identifier.
4. Report the resolved project/workspace, scheme, configuration, device,
   connection transport, DerivedData policy, build result, bundle identifier,
   install result, and launch result. If a stage fails, report that exact stage
   rather than claiming installation succeeded.

Use `--resolve-only` to inspect the complete selection without building,
installing, or launching:

```zsh
<skill-directory>/scripts/install-current-ios-app.sh --resolve-only "$PWD"
```

## Device readiness

Discovery includes connected devices and known paired physical iOS devices and
returns their stable identifiers, names, types, connection states, pairing
states, transports, and recent CoreDevice activity. Codex—not the Python
helper—uses that evidence plus the user's natural language and conversational
context to make the best-effort choice. The installer accepts the resulting
exact name or stable identifier and verifies that it resolves uniquely.

The installer still requires the selected device to become connected before
continuing. For a selected paired device whose transport is
`localNetwork`, it runs a bounded `devicectl device info details` probe and
briefly re-lists devices to allow the wireless tunnel to appear. The installer
never probes an unpaired device.

Connectivity is rechecked after the build before installation and again before
launch. A wireless device may be reactivated at either boundary. Failures name
the blocked stage and distinguish USB, local-network, paired-but-unavailable,
and unpaired states. `--resolve-only` may establish a paired wireless tunnel,
but still does not build, install, or launch.

## Project configuration

Projects may commit a top-level `.ios-install-skill.json` for stable build
selection:

```json
{
  "version": 1,
  "container": "MyApp.xcworkspace",
  "scheme": "MyApp",
  "configuration": "Debug"
}
```

Use a top-level `.ios-install-skill.local.json` for checkout-specific values,
especially the physical device. Keep this file out of version control. The
installer writes the device identifier after the user chooses a device by
name; do not ask the user to create or edit this value directly:

```json
{
  "version": 1,
  "deviceIdentifier": "COREDEVICE-STABLE-IDENTIFIER"
}
```

The local file may override `container`, `scheme`, `configuration`,
or the generated `deviceIdentifier`. A legacy local `deviceName` is accepted
once and migrated to the matched identifier. New configuration never stores a
device name. The committed project file cannot select a personal device. JSON
is parsed with Python's standard library; no third-party parser is required.
When a project adopts the local file, add its name to the project's ignore
policy.

Build-setting resolution precedence is:

1. Environment override.
2. `.ios-install-skill.local.json`.
3. `.ios-install-skill.json`.
4. Unambiguous Xcode discovery.

Device resolution honors a one-run exact `IOS_DEVICE_NAME` or
`IOS_DEVICE_IDENTIFIER`, then a saved local `deviceIdentifier`. If none exists,
Codex enumerates the candidates, chooses one, and reruns with its exact
`IOS_DEVICE_IDENTIFIER`. The deterministic helper never interprets a
natural-language device hint or silently ranks multiple candidates.

Supported environment overrides are `IOS_PROJECT`, `IOS_WORKSPACE`,
`IOS_SCHEME`, `IOS_CONFIGURATION`, `IOS_DEVICE_NAME`,
`IOS_DEVICE_IDENTIFIER`, and `IOS_DERIVED_DATA_PATH`. Ordinary interactive use
should select from the structured device listing and pass the exact identifier;
use an exact name with `--save-device-selection` only when persistence is
desired.

## Build and generation boundaries

Use Xcode's normal DerivedData location unless the current repository or user
explicitly requires a different stable path. Do not redirect DerivedData to a
temporary directory as a sandbox workaround.

The installer builds the current workspace or project as it exists. It does
not infer permission to regenerate checked-in project files. When the current
task explicitly requires XcodeGen regeneration, first preserve unrelated
generated-project edits and invoke the installer with
`IOS_GENERATE_PROJECT=1`.
