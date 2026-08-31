import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HELPER_PATH = Path(__file__).parents[1] / "scripts" / "ios-install-json.py"
SPEC = importlib.util.spec_from_file_location("ios_install_json", HELPER_PATH)
ios_install_json = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ios_install_json)


def device(
    identifier,
    name,
    *,
    connection_state="connected",
    pairing_state="paired",
    transport_type="usb",
    device_type="iPhone",
    last_connection_date=0,
    physical=True,
    platform="iOS",
):
    return {
        "identifier": identifier,
        "properties": {
            "hardware": {
                "platform": platform,
                "reality": "physical" if physical else "simulator",
                "deviceType": device_type,
                "udid": f"UDID-{identifier}",
            },
            "connection": {
                "state": connection_state,
                "pairingState": pairing_state,
                "transportType": transport_type,
                "lastConnectionDate": last_connection_date,
            },
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

        self.assertEqual(selected["identifier"], "CORE-1")
        self.assertEqual(selected["name"], "Alan's iPhone")
        self.assertEqual(selected["connectionState"], "connected")
        self.assertEqual(selected["pairingState"], "paired")
        self.assertEqual(selected["transportType"], "usb")
        self.assertIn("exact name", selected["selectionReason"])

    def test_paired_disconnected_wireless_device_is_a_candidate(self):
        document = listing(
            device(
                "CORE-1",
                "Alan's iPhone",
                connection_state="disconnected",
                transport_type="localNetwork",
            )
        )

        selected = ios_install_json.select_device(document, identifier="CORE-1")

        self.assertEqual(selected["connectionState"], "disconnected")
        self.assertEqual(selected["pairingState"], "paired")
        self.assertEqual(selected["transportType"], "localNetwork")

    def test_connection_descriptions_distinguish_wired_and_wireless(self):
        wired = ios_install_json.select_device(
            listing(device("WIRED", "Wired Phone")),
            identifier="WIRED",
        )
        wireless = ios_install_json.select_device(
            listing(
                device(
                    "WIRELESS",
                    "Wireless Phone",
                    transport_type="localNetwork",
                )
            ),
            identifier="WIRELESS",
        )

        self.assertEqual(
            ios_install_json.describe_device_connection(wired),
            "connected by USB",
        )
        self.assertEqual(
            ios_install_json.describe_device_connection(wireless),
            "connected over local network",
        )

    def test_unpaired_and_unavailable_devices_are_reported_distinctly(self):
        unpaired = ios_install_json.select_device(
            listing(
                device(
                    "UNPAIRED",
                    "Unpaired Phone",
                    connection_state="disconnected",
                    pairing_state="unpaired",
                    transport_type="localNetwork",
                )
            ),
            identifier="UNPAIRED",
        )
        unavailable = ios_install_json.select_device(
            listing(
                device(
                    "UNAVAILABLE",
                    "Unavailable Phone",
                    connection_state="unavailable",
                    transport_type="unknown",
                )
            ),
            identifier="UNAVAILABLE",
        )

        self.assertEqual(
            ios_install_json.describe_device_connection(unpaired),
            "unpaired",
        )
        self.assertFalse(ios_install_json.device_can_activate_wirelessly(unpaired))
        self.assertEqual(
            ios_install_json.describe_device_connection(unavailable),
            "known but unavailable",
        )

    def test_saved_identifier_survives_device_rename(self):
        document = listing(device("CORE-1", "Renamed Phone"))

        selected = ios_install_json.select_device(
            document,
            identifier="CORE-1",
        )

        self.assertEqual(selected["name"], "Renamed Phone")

    def test_saved_identifier_remains_authoritative_over_active_device(self):
        document = listing(
            device("ACTIVE", "Alan's iPhone"),
            device(
                "SAVED",
                "Alan's Dev Phone",
                connection_state="disconnected",
                transport_type="localNetwork",
            ),
        )

        selected = ios_install_json.select_device(document, identifier="SAVED")

        self.assertEqual(selected["identifier"], "SAVED")
        self.assertEqual(selected["selectionReason"], "stable identifier match")

    def test_duplicate_human_readable_names_prefer_connected_device(self):
        document = listing(
            device(
                "OFFLINE",
                "iPhone",
                connection_state="disconnected",
                transport_type="localNetwork",
            ),
            device("ACTIVE", "iPhone"),
        )

        selected = ios_install_json.select_device(document, name="iPhone")

        self.assertEqual(selected["identifier"], "ACTIVE")
        self.assertIn("exact name", selected["selectionReason"])

    def test_first_run_prefers_active_phone_over_offline_devices(self):
        document = listing(
            device(
                "ACTIVE",
                "Alan's iPhone",
                last_connection_date=20,
            ),
            device(
                "DEV",
                "Alan's Dev Phone",
                connection_state="disconnected",
                transport_type="localNetwork",
                last_connection_date=30,
            ),
            device(
                "IPAD",
                "Alan's iPad",
                connection_state="unavailable",
                device_type="iPad",
                last_connection_date=40,
            ),
        )

        selected = ios_install_json.select_device(document)

        self.assertEqual(selected["identifier"], "ACTIVE")
        self.assertIn("connection readiness", selected["selectionReason"])

    def test_natural_language_hint_matches_iphone_and_prefers_active_match(self):
        document = listing(
            device("ACTIVE", "Alan’s iPhone"),
            device(
                "DEV",
                "Alan’s Dev Phone",
                connection_state="disconnected",
                transport_type="localNetwork",
            ),
        )

        selected = ios_install_json.select_device(document, hint="Alan's phone")

        self.assertEqual(selected["identifier"], "ACTIVE")
        self.assertIn("Alan's phone", selected["selectionReason"])

    def test_natural_language_hint_can_select_ipad_over_connected_phone(self):
        document = listing(
            device("PHONE", "Alan's iPhone"),
            device("IPAD", "Alan's iPad", device_type="iPad"),
        )

        selected = ios_install_json.select_device(document, hint="Alan's iPad")

        self.assertEqual(selected["identifier"], "IPAD")

    def test_all_known_physical_ios_devices_are_candidates(self):
        document = listing(
            device("CONNECTED", "Connected"),
            device("OFFLINE", "Offline", connection_state="disconnected"),
            device("SIMULATOR", "Simulator", physical=False),
            device("WATCH", "Watch", platform="watchOS"),
        )

        candidates = ios_install_json.physical_ios_devices(document)

        self.assertEqual(
            [candidate["identifier"] for candidate in candidates],
            ["CONNECTED", "OFFLINE"],
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
