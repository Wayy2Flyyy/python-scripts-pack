"""Plugin runner for advanced script examples."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[3]))

from shared.helpers import pretty_kv_print, safe_read_json

CONFIG_PATH = Path(__file__).with_name("plugin_config.json")
PLUGIN_PACKAGE = "scripts.advanced.plugin_runner.plugins"


def load_config() -> dict[str, Any]:
    return safe_read_json(CONFIG_PATH)


def get_enabled_plugins(config: dict[str, Any]) -> list[str]:
    enabled = config.get("enabled_plugins", [])
    if not isinstance(enabled, list):
        raise ValueError("enabled_plugins must be a list")
    return [str(name) for name in enabled]


def get_plugin_settings(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    settings = config.get("plugin_settings", {})
    if not isinstance(settings, dict):
        raise ValueError("plugin_settings must be an object")
    return {str(name): dict(value) for name, value in settings.items()}


def load_plugin(module_name: str):
    try:
        return importlib.import_module(f"{PLUGIN_PACKAGE}.{module_name}")
    except ModuleNotFoundError as exc:
        print(f"Error: plugin '{module_name}' could not be imported: {exc}")
        return None


def run_plugin(module_name: str, settings: dict[str, Any]) -> dict[str, Any] | None:
    module = load_plugin(module_name)
    if module is None:
        return None

    if not hasattr(module, "run"):
        print(f"Error: plugin '{module_name}' has no run(config) function")
        return None

    try:
        return module.run(settings)
    except KeyError as exc:
        print(f"Error: plugin '{module_name}' missing config key: {exc}")
        return None
    except ValueError as exc:
        print(f"Error: plugin '{module_name}' config error: {exc}")
        return None
    except Exception as exc:
        print(f"Error: plugin '{module_name}' failed: {exc}")
        return None


def print_results(module_name: str, results: dict[str, Any]) -> None:
    print(f"=== plugin: {module_name} ===")
    if not results:
        print("(no output)")
        return
    if isinstance(results, dict) and "items" in results and isinstance(
        results["items"], list
    ):
        items = results.get("items", [])
        output = {k: v for k, v in results.items() if k != "items"}
        pretty_kv_print({k: str(v) for k, v in output.items()})
        print("items:")
        for item in items:
            print(f"  {item}")
        return
    pretty_kv_print({k: str(v) for k, v in results.items()})


def main() -> None:
    try:
        config = load_config()
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    enabled = get_enabled_plugins(config)
    settings = get_plugin_settings(config)

    for module_name in enabled:
        plugin_settings = settings.get(module_name, {})
        results = run_plugin(module_name, plugin_settings)
        if results is not None:
            print_results(module_name, results)


if __name__ == "__main__":
    main()
