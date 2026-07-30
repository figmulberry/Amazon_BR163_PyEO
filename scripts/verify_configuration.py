from __future__ import annotations

import argparse
import configparser
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CheckResult:
    """Result of one configuration validation check."""

    name: str
    passed: bool
    detail: str


REQUIRED_SECTIONS = (
    "run_mode",
    "forest_sentinel",
    "environment",
    "raster_processing_parameters",
    "vector_processing_parameters",
    "alerts_sending_options",
)

PROCESSING_FLAGS = (
    "do_tile_intersection",
    "do_raster",
    "do_build_composite",
    "do_download",
    "do_classify",
    "do_change",
    "do_delete_existing_vector",
    "do_vectorise",
    "do_integrate",
    "do_filter",
    "do_distribution",
)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    default_config = (
        Path(__file__).resolve().parents[1]
        / "00_admin"
        / "amazon_br163_working.ini"
    )

    parser = argparse.ArgumentParser(
        description=(
            "Validate the Amazon BR-163 PyEO repository configuration "
            "without running the processing pipeline."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help=(
            "Path to the INI configuration file. Defaults to "
            "00_admin/amazon_br163_working.ini."
        ),
    )
    return parser.parse_args()


def normalise_path(raw_value: str) -> Path:
    """Convert an INI path value into a Path object."""

    return Path(raw_value.strip().strip('"').strip("'")).expanduser()


def check_path(
    name: str,
    path: Path,
    *,
    expected_type: str,
) -> CheckResult:
    """Check whether a required file-system path exists."""

    if expected_type == "file":
        passed = path.is_file()
        expectation = "file"
    elif expected_type == "directory":
        passed = path.is_dir()
        expectation = "directory"
    else:
        raise ValueError(f"Unsupported expected path type: {expected_type}")

    if passed:
        detail = str(path)
    else:
        detail = f"Expected {expectation} not found: {path}"

    return CheckResult(name=name, passed=passed, detail=detail)


def get_required_value(
    config: configparser.ConfigParser,
    section: str,
    option: str,
) -> tuple[str | None, CheckResult]:
    """Read a required INI value and report whether it is available."""

    if not config.has_section(section):
        return None, CheckResult(
            name=f"Configuration value [{section}] {option}",
            passed=False,
            detail=f"Missing section: [{section}]",
        )

    if not config.has_option(section, option):
        return None, CheckResult(
            name=f"Configuration value [{section}] {option}",
            passed=False,
            detail=f"Missing option: [{section}] {option}",
        )

    value = config.get(section, option).strip()

    if not value:
        return None, CheckResult(
            name=f"Configuration value [{section}] {option}",
            passed=False,
            detail=f"Empty option: [{section}] {option}",
        )

    return value, CheckResult(
        name=f"Configuration value [{section}] {option}",
        passed=True,
        detail=value,
    )


def validate_sections(
    config: configparser.ConfigParser,
) -> list[CheckResult]:
    """Validate that all required INI sections exist."""

    results: list[CheckResult] = []

    for section in REQUIRED_SECTIONS:
        results.append(
            CheckResult(
                name=f"Configuration section [{section}]",
                passed=config.has_section(section),
                detail=(
                    "Present"
                    if config.has_section(section)
                    else f"Missing section: [{section}]"
                ),
            )
        )

    return results


def validate_configured_paths(
    config: configparser.ConfigParser,
) -> list[CheckResult]:
    """Validate configured files and directories."""

    results: list[CheckResult] = []

    path_definitions = (
        ("forest_sentinel", "model", "Model file", "file"),
        ("environment", "pyeo_dir", "PyEO source directory", "directory"),
        ("environment", "tile_dir", "Tile data directory", "directory"),
        ("environment", "integrated_dir", "Integrated output directory", "directory"),
        ("environment", "roi_dir", "ROI directory", "directory"),
        ("environment", "geometry_dir", "Reference geometry directory", "directory"),
        ("environment", "log_dir", "Log directory", "directory"),
        ("environment", "credentials_path", "Credentials file", "file"),
        ("environment", "conda_directory", "Conda installation directory", "directory"),
    )

    for section, option, label, expected_type in path_definitions:
        value, value_result = get_required_value(config, section, option)

        if value is None:
            results.append(value_result)
            continue

        results.append(
            check_path(
                label,
                normalise_path(value),
                expected_type=expected_type,
            )
        )

    roi_dir_value, _ = get_required_value(config, "environment", "roi_dir")
    roi_filename, _ = get_required_value(
        config,
        "environment",
        "roi_filename",
    )

    if roi_dir_value and roi_filename:
        roi_path = normalise_path(roi_dir_value) / roi_filename
        results.append(check_path("ROI file", roi_path, expected_type="file"))

    geometry_dir_value, _ = get_required_value(
        config,
        "environment",
        "geometry_dir",
    )
    level_1_filename, _ = get_required_value(
        config,
        "vector_processing_parameters",
        "level_1_filename",
    )

    if geometry_dir_value and level_1_filename:
        level_1_path = (
            normalise_path(geometry_dir_value)
            / Path(level_1_filename.replace("\\", "/"))
        )
        results.append(
            check_path(
                "ADM1 reference file",
                level_1_path,
                expected_type="file",
            )
        )

    return results


def validate_processing_flags(
    config: configparser.ConfigParser,
) -> list[CheckResult]:
    """Check how many processing stages are enabled."""

    enabled_flags: list[str] = []

    for section in (
        "raster_processing_parameters",
        "vector_processing_parameters",
        "alerts_sending_options",
    ):
        if not config.has_section(section):
            continue

        for flag in PROCESSING_FLAGS:
            if config.has_option(section, flag):
                try:
                    if config.getboolean(section, flag):
                        enabled_flags.append(f"[{section}] {flag}")
                except ValueError:
                    return [
                        CheckResult(
                            name="Processing-stage flags",
                            passed=False,
                            detail=(
                                f"Invalid Boolean value for "
                                f"[{section}] {flag}"
                            ),
                        )
                    ]

    if len(enabled_flags) == 0:
        return [
            CheckResult(
                name="Processing-stage flags",
                passed=True,
                detail="All monitored processing flags are disabled.",
            )
        ]

    if len(enabled_flags) == 1:
        return [
            CheckResult(
                name="Processing-stage flags",
                passed=True,
                detail=f"One processing flag is enabled: {enabled_flags[0]}",
            )
        ]

    return [
        CheckResult(
            name="Processing-stage flags",
            passed=False,
            detail=(
                "Multiple processing flags are enabled: "
                + ", ".join(enabled_flags)
            ),
        )
    ]


def print_results(results: Iterable[CheckResult]) -> int:
    """Print results and return a process exit code."""

    result_list = list(results)

    print()
    print("Amazon BR-163 PyEO Configuration Validation")
    print("=" * 47)

    for result in result_list:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}")
        print(f"       {result.detail}")

    failed_count = sum(not result.passed for result in result_list)

    print()
    print("-" * 47)

    if failed_count == 0:
        print("Configuration validation passed.")
        return 0

    print(
        f"Configuration validation failed with "
        f"{failed_count} failed check(s)."
    )
    return 1


def main() -> int:
    """Run all non-destructive configuration checks."""

    args = parse_arguments()
    repository_root = Path(__file__).resolve().parents[1]
    config_path = args.config.resolve()

    results: list[CheckResult] = [
        check_path(
            "Repository root",
            repository_root,
            expected_type="directory",
        ),
        check_path(
            "Configuration file",
            config_path,
            expected_type="file",
        ),
    ]

    if not config_path.is_file():
        return print_results(results)

    config = configparser.ConfigParser(interpolation=None)

    try:
        with config_path.open("r", encoding="utf-8-sig") as config_file:
            config.read_file(config_file)
    except (OSError, configparser.Error) as exc:
        results.append(
            CheckResult(
                name="Configuration parsing",
                passed=False,
                detail=str(exc),
            )
        )
        return print_results(results)

    results.append(
        CheckResult(
            name="Configuration parsing",
            passed=True,
            detail=f"Loaded: {config_path}",
        )
    )

    results.extend(validate_sections(config))
    results.extend(validate_configured_paths(config))
    results.extend(validate_processing_flags(config))

    return print_results(results)


if __name__ == "__main__":
    sys.exit(main())