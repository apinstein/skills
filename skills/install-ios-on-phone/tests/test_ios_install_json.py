import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HELPER_PATH = Path(__file__).parents[1] / "scripts" / "ios-install-json.py"
SPEC = importlib.util.spec_from_file_location("ios_install_json", HELPER_PATH)
ios_install_json = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ios_install_json)


def device(identifier, name, *, connected=True, physical=True, platform="iOS"):
    return {
        "identifier": identifier,
        "properties": {
            "hardware": {
                "platform": platform,
                "reality": "physical" if physical else "simulator",
                "udid": f"UDID-{identifier}",
            },
            "connection": {"state": "connected" if connected else "disconnected"},
            "state": {"name": name},
        },
    }


def listing(*devices):
    return {"result": {"devices": list(devices)}}


class DeviceResolutionTests(unittest.TestCase):
    def test_name_selection_returns_coredevice_identifier(self):
        document = listing(device("CORE-1", "Alan's iPhone"))

        selected = ios_install_json.select_device(
            document,
            name="Alan's iPhone",
        )

        self.assertEqual(
            selected,
            {"identifier": "CORE-1", "name": "Alan's iPhone"},
        )

    def test_saved_identifier_survives_device_rename(self):
        document = listing(device("CORE-1", "Renamed Phone"))

        selected = ios_install_json.select_device(
            document,
            identifier="CORE-1",
        )

        self.assertEqual(selected["name"], "Renamed Phone")

    def test_duplicate_human_readable_names_are_ambiguous(self):
        document = listing(
            device("CORE-1", "iPhone"),
            device("CORE-2", "iPhone"),
        )

        with self.assertRaises(ios_install_json.DeviceResolutionError) as context:
            ios_install_json.select_device(document, name="iPhone")

        self.assertEqual(context.exception.exit_code, 2)
        self.assertIn("CORE-1", str(context.exception))
        self.assertIn("CORE-2", str(context.exception))

    def test_first_run_requires_explicit_device_choice(self):
        document = listing(device("CORE-1", "Only Phone"))

        with self.assertRaises(ios_install_json.DeviceResolutionError) as context:
            ios_install_json.select_device(document)

        self.assertEqual(context.exception.exit_code, 2)
        self.assertIn("choose", str(context.exception))

    def test_only_connected_physical_ios_devices_are_candidates(self):
        document = listing(
            device("CONNECTED", "Connected"),
            device("OFFLINE", "Offline", connected=False),
            device("SIMULATOR", "Simulator", physical=False),
            device("WATCH", "Watch", platform="watchOS"),
        )

        self.assertEqual(
            ios_install_json.connected_physical_ios_devices(document),
            [{"identifier": "CONNECTED", "name": "Connected"}],
        )


class ConfigurationTests(unittest.TestCase):
    def test_committed_project_configuration_cannot_select_a_device(self):
        with self.assertRaises(ios_install_json.ConfigError):
            ios_install_json.validate_config_document(
                {"version": 1, "deviceIdentifier": "CORE-1"},
                "project",
            )

    def test_local_configuration_rejects_name_and_identifier_together(self):
        with self.assertRaises(ios_install_json.ConfigError):
            ios_install_json.validate_config_document(
                {
                    "version": 1,
                    "deviceName": "Alan's iPhone",
                    "deviceIdentifier": "CORE-1",
                },
                "local",
            )

    def test_unknown_configuration_keys_are_rejected(self):
        with self.assertRaises(ios_install_json.ConfigError):
            ios_install_json.validate_config_document(
                {"version": 1, "scheem": "Typo"},
                "project",
            )

    def test_saving_identifier_migrates_legacy_name_and_preserves_overrides(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".ios-install-skill.local.json"
            path.write_text(
                json.dumps(
                    {
                        "configuration": "Release",
                        "deviceName": "Alan's iPhone",
                    }
                ),
                encoding="utf-8",
            )

            ios_install_json.save_device_config(path, "CORE-1")

            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                saved,
                {
                    "configuration": "Release",
                    "deviceIdentifier": "CORE-1",
                    "version": 1,
                },
            )


if __name__ == "__main__":
    unittest.main()
