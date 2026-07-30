from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


PLACEHOLDERS = (
    "{{PROJECT_ROOT}}",
    "{{PYEO_DIR}}",
    "{{DATA_ROOT}}",
    "{{LOG_DIR}}",
    "{{CREDENTIALS_PATH}}",
    "{{CONDA_DIRECTORY}}",
    "{{CONDA_ENV_NAME}}",
)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    repository_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description=(
            "Generate a machine-specific Amazon BR-163 PyEO configuration "
            "without modifying the validated Version 1.0 configuration."
        )
    )

    parser.add_argument(
        "--template",
        type=Path,
        default=(
            repository_root
            / "00_starting_files"
            / "templates"
            / "amazon_br163_pyeo_local.template.ini"
        ),
        help="Path to the portable configuration template.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=repository_root / "00_admin" / "amazon_br163_local.ini",
        help="Path for the generated local configuration.",
    )

    parser.add_argument(
        "--pyeo-dir",
        type=Path,
        help="Path to the local PyEO source checkout.",
    )

    parser.add_argument(
        "--data-root",
        type=Path,
        help="Root directory for local Amazon BR-163 processing data.",
    )

    parser.add_argument(
        "--log-dir",
        type=Path,
        help="Directory for runtime logs.",
    )

    parser.add_argument(
        "--credentials-path",
        type=Path,
        help="Path to the local Copernicus Data Space credentials file.",
    )

    parser.add_argument(
        "--conda-directory",
        type=Path,
        help="Path to the local Miniconda or Anaconda installation.",
    )

    parser.add_argument(
        "--conda-env-name",
        default=None,
        help="Name of the Conda environment. Default: pyeo_env.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file without asking for confirmation.",
    )

    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Do not run verify_configuration.py after generation.",
    )

    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help=(
            "Do not prompt for missing values. Missing values use detected "
            "or documented defaults."
        ),
    )

    return parser.parse_args()


def detect_conda_directory() -> Path:
    """Try to determine the active or installed Conda root directory."""

    conda_prefix = os.environ.get("CONDA_PREFIX")

    if conda_prefix:
        prefix_path = Path(conda_prefix).expanduser().resolve()

        if prefix_path.parent.name.lower() == "envs":
            return prefix_path.parent.parent

        return prefix_path

    conda_exe = os.environ.get("CONDA_EXE")

    if conda_exe:
        executable_path = Path(conda_exe).expanduser().resolve()
        return executable_path.parent.parent

    candidates = (
        Path.home() / "miniconda3",
        Path.home() / "anaconda3",
        Path("C:/ProgramData/miniconda3"),
        Path("C:/ProgramData/anaconda3"),
    )

    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()

    return (Path.home() / "miniconda3").resolve()


def prompt_for_path(
    label: str,
    suggested: Path,
    *,
    non_interactive: bool,
) -> Path:
    """Prompt for a path while offering a detected or documented default."""

    suggested = suggested.expanduser().resolve()

    if non_interactive:
        return suggested

    response = input(
        f"{label}\nPress Enter to use: {suggested}\n> "
    ).strip()

    if not response:
        return suggested

    return Path(response).expanduser().resolve()


def prompt_for_text(
    label: str,
    suggested: str,
    *,
    non_interactive: bool,
) -> str:
    """Prompt for a text value while offering a default."""

    if non_interactive:
        return suggested

    response = input(
        f"{label}\nPress Enter to use: {suggested}\n> "
    ).strip()

    return response or suggested


def confirm_overwrite(output_path: Path, *, force: bool) -> bool:
    """Confirm replacement of an existing local configuration."""

    if not output_path.exists():
        return True

    if force:
        return True

    response = input(
        f"\nLocal configuration already exists:\n{output_path}\n"
        "Overwrite it? [y/N]\n> "
    ).strip().lower()

    return response in {"y", "yes"}


def replace_placeholders(
    template_text: str,
    replacements: dict[str, str],
) -> str:
    """Replace all supported template placeholders."""

    rendered = template_text

    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)

    unresolved = [
        placeholder
        for placeholder in PLACEHOLDERS
        if placeholder in rendered
    ]

    if unresolved:
        unresolved_text = ", ".join(unresolved)
        raise ValueError(
            f"Unresolved configuration placeholders: {unresolved_text}"
        )

    return rendered


def display_configuration_summary(
    *,
    repository_root: Path,
    pyeo_dir: Path,
    data_root: Path,
    log_dir: Path,
    credentials_path: Path,
    conda_directory: Path,
    conda_env_name: str,
    output_path: Path,
) -> None:
    """Display the values that will be written."""

    print()
    print("Local Configuration Summary")
    print("=" * 48)
    print(f"Repository root:    {repository_root}")
    print(f"PyEO source:        {pyeo_dir}")
    print(f"Data root:          {data_root}")
    print(f"Log directory:      {log_dir}")
    print(f"Credentials file:   {credentials_path}")
    print(f"Conda directory:    {conda_directory}")
    print(f"Conda environment:  {conda_env_name}")
    print(f"Output file:        {output_path}")
    print("=" * 48)


def run_validator(repository_root: Path, output_path: Path) -> int:
    """Run the non-destructive configuration validator."""

    validator_path = (
        repository_root / "scripts" / "verify_configuration.py"
    )

    if not validator_path.is_file():
        print()
        print(
            "[WARN] Configuration generated, but the validator was not found:"
        )
        print(f"       {validator_path}")
        return 0

    print()
    print("Running configuration validation...")
    print()

    completed = subprocess.run(
        [
            sys.executable,
            str(validator_path),
            "--config",
            str(output_path),
        ],
        check=False,
    )

    return completed.returncode


def main() -> int:
    """Generate and optionally validate a local INI configuration."""

    args = parse_arguments()

    repository_root = Path(__file__).resolve().parents[1]
    template_path = args.template.expanduser().resolve()
    output_path = args.output.expanduser().resolve()

    print()
    print("Amazon BR-163 PyEO Local Configuration Generator")
    print("=" * 52)
    print(f"Repository detected: {repository_root}")

    if not template_path.is_file():
        print()
        print("[FAIL] Configuration template not found:")
        print(f"       {template_path}")
        return 1

    default_pyeo_dir = Path("C:/GIS/src/pyeo")
    default_data_root = Path("C:/GIS/data/Amazon_BR163_PyEO")
    default_log_dir = Path("C:/GIS/logs")
    default_credentials_path = Path("C:/GIS/secrets/pyeo_cdse.ini")
    default_conda_directory = detect_conda_directory()

    pyeo_dir = (
        args.pyeo_dir.expanduser().resolve()
        if args.pyeo_dir
        else prompt_for_path(
            "Where is the local PyEO source checkout?",
            default_pyeo_dir,
            non_interactive=args.non_interactive,
        )
    )

    data_root = (
        args.data_root.expanduser().resolve()
        if args.data_root
        else prompt_for_path(
            "Where should Sentinel-2 processing data be stored?",
            default_data_root,
            non_interactive=args.non_interactive,
        )
    )

    log_dir = (
        args.log_dir.expanduser().resolve()
        if args.log_dir
        else prompt_for_path(
            "Where should runtime logs be stored?",
            default_log_dir,
            non_interactive=args.non_interactive,
        )
    )

    credentials_path = (
        args.credentials_path.expanduser().resolve()
        if args.credentials_path
        else prompt_for_path(
            "Where is the Copernicus Data Space credentials file?",
            default_credentials_path,
            non_interactive=args.non_interactive,
        )
    )

    conda_directory = (
        args.conda_directory.expanduser().resolve()
        if args.conda_directory
        else prompt_for_path(
            "Where is Miniconda or Anaconda installed?",
            default_conda_directory,
            non_interactive=args.non_interactive,
        )
    )

    conda_env_name = (
        args.conda_env_name
        or prompt_for_text(
            "What is the Conda environment name?",
            "pyeo_env",
            non_interactive=args.non_interactive,
        )
    )

    display_configuration_summary(
        repository_root=repository_root,
        pyeo_dir=pyeo_dir,
        data_root=data_root,
        log_dir=log_dir,
        credentials_path=credentials_path,
        conda_directory=conda_directory,
        conda_env_name=conda_env_name,
        output_path=output_path,
    )

    if not confirm_overwrite(output_path, force=args.force):
        print()
        print("Configuration generation cancelled. No files were changed.")
        return 0

    try:
        template_text = template_path.read_text(encoding="utf-8-sig")

        replacements = {
            "{{PROJECT_ROOT}}": str(repository_root),
            "{{PYEO_DIR}}": str(pyeo_dir),
            "{{DATA_ROOT}}": str(data_root),
            "{{LOG_DIR}}": str(log_dir),
            "{{CREDENTIALS_PATH}}": str(credentials_path),
            "{{CONDA_DIRECTORY}}": str(conda_directory),
            "{{CONDA_ENV_NAME}}": conda_env_name,
        }

        rendered_configuration = replace_placeholders(
            template_text,
            replacements,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            rendered_configuration,
            encoding="utf-8",
            newline="\n",
        )

    except (OSError, ValueError) as exc:
        print()
        print("[FAIL] Local configuration could not be generated.")
        print(f"       {exc}")
        return 1

    print()
    print("[PASS] Local configuration generated:")
    print(f"       {output_path}")

    if args.no_validate:
        print()
        print("Automatic validation was skipped.")
        return 0

    return run_validator(repository_root, output_path)


if __name__ == "__main__":
    sys.exit(main())