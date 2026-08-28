import json
import os
import plistlib
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).parents[1]
INSTALLER_PATH = SKILL_ROOT / "scripts" / "install-current-ios-app.sh"


def device_listing(
    *,
    name="Test Phone",
    connection_state="connected",
    pairing_state="paired",
    transport_type="localNetwork",
):
    return {
        "result": {
            "devices": [
                {
                    "identifier": "CORE-1",
                    "properties": {
                        "connection": {
                            "state": connection_state,
                            "pairingState": pairing_state,
                            "transportType": transport_type,
                        },
                        "hardware": {
                            "platform": "iOS",
                            "reality": "physical",
                        },
                        "state": {"name": name},
                    },
                }
            ]
        }
    }


def write_executable(path, contents):
    path.write_text(contents, encoding="utf-8")
    path.chmod(0o755)


class InstallerConnectivityTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.repository = self.root / "repository"
        self.repository.mkdir()
        (self.repository / "TestApp.xcodeproj").mkdir()

        self.app_directory = self.root / "Build" / "TestApp.app"
        self.app_directory.mkdir(parents=True)
        with (self.app_directory / "Info.plist").open("wb") as stream:
            plistlib.dump({"CFBundleIdentifier": "example.TestApp"}, stream)

        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        self.log_path = self.root / "commands.log"
        self.listings_path = self.root / "device-listings.json"
        self.listing_index_path = self.root / "device-listing-index"

        write_executable(
            self.fake_bin / "xcrun",
            r"""#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

arguments = sys.argv[1:]
log_path = Path(os.environ["FAKE_COMMAND_LOG"])
with log_path.open("a", encoding="utf-8") as stream:
    stream.write("xcrun " + " ".join(arguments) + "\n")

if arguments[:3] == ["devicectl", "list", "devices"]:
    listings = json.loads(Path(os.environ["FAKE_DEVICE_LISTINGS"]).read_text())
    index_path = Path(os.environ["FAKE_DEVICE_LISTING_INDEX"])
    index = int(index_path.read_text()) if index_path.exists() else 0
    if index >= len(listings):
        index = len(listings) - 1
    json.dump(listings[index], sys.stdout)
    index_path.write_text(str(index + 1))
elif arguments[:4] == ["devicectl", "device", "info", "details"]:
    if os.environ.get("FAKE_PROBE_FAILURE") == "1":
        print("simulated wireless activation timeout", file=sys.stderr)
        raise SystemExit(1)
elif arguments[:4] in (
    ["devicectl", "device", "install", "app"],
    ["devicectl", "device", "process", "launch"],
):
    pass
else:
    print(f"unexpected xcrun arguments: {arguments}", file=sys.stderr)
    raise SystemExit(2)
""",
        )
        write_executable(
            self.fake_bin / "xcodebuild",
            """#!/bin/zsh
print -r -- "xcodebuild $*" >> "$FAKE_COMMAND_LOG"
if [[ " $* " == *" -showBuildSettings "* ]]; then
  print -r -- "$FAKE_BUILD_SETTINGS"
  exit 0
fi
if [[ "$1" == "build" ]]; then
  exit 0
fi
print -u2 -- "unexpected xcodebuild arguments: $*"
exit 2
""",
        )
        write_executable(
            self.fake_bin / "sleep",
            """#!/bin/zsh
print -r -- "sleep $*" >> "$FAKE_COMMAND_LOG"
""",
        )

    def run_installer(self, listings, *, probe_failure=False):
        self.listings_path.write_text(json.dumps(listings), encoding="utf-8")
        build_settings = [
            {
                "buildSettings": {
                    "PLATFORM_NAME": "iphoneos",
                    "PRODUCT_TYPE": "com.apple.product-type.application",
                    "SUPPORTED_PLATFORMS": "iphoneos",
                    "TARGET_BUILD_DIR": str(self.app_directory.parent),
                    "WRAPPER_EXTENSION": "app",
                    "WRAPPER_NAME": self.app_directory.name,
                }
            }
        ]
        environment = os.environ.copy()
        environment.update(
            {
                "FAKE_BUILD_SETTINGS": json.dumps(build_settings),
                "FAKE_COMMAND_LOG": str(self.log_path),
                "FAKE_DEVICE_LISTINGS": str(self.listings_path),
                "FAKE_DEVICE_LISTING_INDEX": str(self.listing_index_path),
                "FAKE_PROBE_FAILURE": "1" if probe_failure else "0",
                "IOS_CONFIGURATION": "Debug",
                "IOS_DEVICE_IDENTIFIER": "CORE-1",
                "IOS_PROJECT": "TestApp.xcodeproj",
                "IOS_SCHEME": "TestApp",
                "PATH": f"{self.fake_bin}:{environment['PATH']}",
            }
        )
        return subprocess.run(
            [str(INSTALLER_PATH), str(self.repository)],
            capture_output=True,
            check=False,
            env=environment,
            text=True,
        )

    def command_log(self):
        return self.log_path.read_text(encoding="utf-8").splitlines()

    def test_paired_wireless_probe_timeout_is_actionable(self):
        result = self.run_installer(
            [device_listing(connection_state="disconnected")],
            probe_failure=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Activating paired wireless device", result.stdout)
        self.assertIn(
            "paired wireless but activation failed before build within 10s",
            result.stderr,
        )
        probe_command = next(
            command for command in self.command_log() if "device info details" in command
        )
        self.assertIn("--timeout 10", probe_command)
        self.assertFalse(
            any(command.startswith("xcodebuild build ") for command in self.command_log())
        )

    def test_reactivates_device_before_install_and_launch(self):
        result = self.run_installer(
            [
                device_listing(),
                device_listing(connection_state="disconnected"),
                device_listing(),
                device_listing(connection_state="disconnected"),
                device_listing(),
            ]
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Activating paired wireless device"), 2)
        coredevice_actions = []
        for command in self.command_log():
            if command.startswith("xcrun devicectl list devices"):
                coredevice_actions.append("list")
            elif "device info details" in command:
                coredevice_actions.append("probe")
            elif "device install app" in command:
                coredevice_actions.append("install")
            elif "device process launch" in command:
                coredevice_actions.append("launch")
        self.assertEqual(
            coredevice_actions,
            [
                "list",
                "list",
                "probe",
                "list",
                "install",
                "list",
                "probe",
                "list",
                "launch",
            ],
        )
        self.assertIn(
            "Installed and launched example.TestApp on Test Phone.",
            result.stdout,
        )

    def test_retries_enumeration_while_wireless_tunnel_appears(self):
        result = self.run_installer(
            [
                device_listing(connection_state="disconnected"),
                device_listing(connection_state="disconnected"),
                device_listing(),
            ]
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Activating paired wireless device"), 1)
        self.assertIn("sleep 1", self.command_log())


if __name__ == "__main__":
    unittest.main()
