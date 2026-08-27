#!/usr/bin/env python3

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path


APPLICATION_PRODUCT_TYPE = "com.apple.product-type.application"
PROJECT_CONFIG_KEYS = {"version", "container", "scheme", "configuration"}
LOCAL_CONFIG_KEYS = PROJECT_CONFIG_KEYS | {"deviceIdentifier", "deviceName"}
STRING_CONFIG_KEYS = LOCAL_CONFIG_KEYS - {"version"}


class ConfigError(ValueError):
    pass


class DeviceResolutionError(ValueError):
    def __init__(self, message, exit_code=3):
        super().__init__(message)
        self.exit_code = exit_code


def read_json():
    return json.load(sys.stdin)


def validate_config_document(document, kind):
    if not isinstance(document, dict):
        raise ConfigError("configuration must be a JSON object")

    allowed_keys = PROJECT_CONFIG_KEYS if kind == "project" else LOCAL_CONFIG_KEYS
    unknown_keys = sorted(set(document) - allowed_keys)
    if unknown_keys:
        raise ConfigError(f"unsupported configuration keys: {', '.join(unknown_keys)}")

    version = document.get("version", 1)
    if type(version) is not int or version != 1:
        raise ConfigError(f"unsupported configuration version: {version!r}")

    for key in sorted(STRING_CONFIG_KEYS & set(document)):
        value = document[key]
        if not isinstance(value, str) or not value.strip():
            raise ConfigError(f"{key} must be a non-empty string")

    if kind == "local" and {"deviceName", "deviceIdentifier"} <= set(document):
        raise ConfigError("set only one of deviceName or deviceIdentifier")

    return document


def read_config(path, kind):
    try:
        with Path(path).open(encoding="utf-8") as stream:
            document = json.load(stream)
    except (OSError, json.JSONDecodeError) as error:
        raise ConfigError(str(error)) from error
    return validate_config_document(document, kind)


def validate_config(path, kind):
    try:
        read_config(path, kind)
    except ConfigError as error:
        print(f"error: invalid {kind} configuration {path}: {error}", file=sys.stderr)
        raise SystemExit(2)


def save_device_config(path, identifier):
    config_path = Path(path)
    if config_path.exists():
        document = read_config(config_path, "local")
    else:
        document = {}

    document["version"] = 1
    document["deviceIdentifier"] = identifier
    document.pop("deviceName", None)
    validate_config_document(document, "local")

    config_path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_path = tempfile.mkstemp(
        dir=config_path.parent,
        prefix=f".{config_path.name}.",
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary_path, config_path)
    except BaseException:
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass
        raise


def schemes(container_kind):
    document = read_json()
    for scheme in document.get(container_kind, {}).get("schemes", []):
        print(scheme)


def ios_application_records(document):
    records = []
    for record in document:
        settings = record.get("buildSettings", {})
        supported_platforms = settings.get("SUPPORTED_PLATFORMS", "").split()
        if (
            settings.get("PRODUCT_TYPE") == APPLICATION_PRODUCT_TYPE
            and "iphoneos" in supported_platforms
        ):
            records.append(settings)
    return records


def has_ios_application():
    raise SystemExit(0 if ios_application_records(read_json()) else 1)


def app_product():
    records = [
        settings
        for settings in ios_application_records(read_json())
        if settings.get("PLATFORM_NAME") == "iphoneos"
        and settings.get("WRAPPER_EXTENSION") == "app"
    ]
    if len(records) != 1:
        print(
            f"error: expected one built iOS app product, found {len(records)}",
            file=sys.stderr,
        )
        raise SystemExit(2)

    settings = records[0]
    print(
        json.dumps(
            {
                "targetBuildDirectory": settings["TARGET_BUILD_DIR"],
                "wrapperName": settings["WRAPPER_NAME"],
            }
        )
    )


def connected_physical_ios_devices(document):
    matches = []
    for device in document.get("result", {}).get("devices", []):
        properties = device.get("properties", {})
        hardware = properties.get("hardware", {})
        connection = properties.get("connection", {})
        state = properties.get("state", {})
        if (
            hardware.get("platform") == "iOS"
            and hardware.get("reality") == "physical"
            and connection.get("state") == "connected"
        ):
            matches.append(
                {
                    "identifier": device.get("identifier"),
                    "name": state.get("name"),
                }
            )
    return matches


def select_device(document, name=None, identifier=None):
    if name and identifier:
        raise DeviceResolutionError("set only one device name or identifier", exit_code=2)
    if not name and not identifier:
        raise DeviceResolutionError("choose a connected physical iOS device", exit_code=2)

    matches = connected_physical_ios_devices(document)
    if name:
        matches = [device for device in matches if device["name"] == name]
    if identifier:
        matches = [device for device in matches if device["identifier"] == identifier]

    if len(matches) == 1:
        return matches[0]

    if not matches:
        selector = name or identifier or "automatic discovery"
        raise DeviceResolutionError(
            f"no connected physical iOS device matches {selector!r}"
        )

    candidates = "\n".join(
        f"  {device['name']} ({device['identifier']})" for device in matches
    )
    raise DeviceResolutionError(
        f"multiple connected physical iOS devices match:\n{candidates}",
        exit_code=2,
    )


def resolve_device(name, identifier):
    try:
        device = select_device(read_json(), name, identifier)
    except DeviceResolutionError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(error.exit_code)
    print(json.dumps(device))


def list_devices():
    devices = connected_physical_ios_devices(read_json())
    if not devices:
        print("No connected physical iOS devices were found.")
        return
    print("Connected physical iOS devices:")
    for device in devices:
        print(f"  {device['name']} ({device['identifier']})")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    schemes_parser = subparsers.add_parser("schemes")
    schemes_parser.add_argument("container_kind", choices=("project", "workspace"))
    subparsers.add_parser("has-ios-application")
    subparsers.add_parser("app-product")
    device_parser = subparsers.add_parser("resolve-device")
    device_parser.add_argument("--name")
    device_parser.add_argument("--identifier")
    subparsers.add_parser("list-devices")
    validate_parser = subparsers.add_parser("validate-config")
    validate_parser.add_argument("kind", choices=("project", "local"))
    validate_parser.add_argument("path")
    save_parser = subparsers.add_parser("save-device-config")
    save_parser.add_argument("path")
    save_parser.add_argument("identifier")

    arguments = parser.parse_args()
    if arguments.command == "schemes":
        schemes(arguments.container_kind)
    elif arguments.command == "has-ios-application":
        has_ios_application()
    elif arguments.command == "app-product":
        app_product()
    elif arguments.command == "resolve-device":
        resolve_device(arguments.name, arguments.identifier)
    elif arguments.command == "list-devices":
        list_devices()
    elif arguments.command == "validate-config":
        validate_config(arguments.path, arguments.kind)
    elif arguments.command == "save-device-config":
        try:
            save_device_config(arguments.path, arguments.identifier)
        except ConfigError as error:
            print(f"error: could not save device selection: {error}", file=sys.stderr)
            raise SystemExit(2)


if __name__ == "__main__":
    main()
