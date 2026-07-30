#!/usr/bin/env python
"""Verify that the active Python environment can import PyEO's core stack.

Run from Miniconda/Anaconda Prompt after:
    conda activate pyeo_env
    python verify_pyeo_installation.py

This script never changes the environment. It only reports diagnostics.
"""
from __future__ import annotations

import importlib
import importlib.metadata
import os
import platform
import shutil
import sys
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Check:
    name: str
    action: Callable[[], str]
    required: bool = True


def package_version(distribution: str) -> str:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "distribution metadata not found"


def import_report(module_name: str, distribution: Optional[str] = None) -> str:
    module = importlib.import_module(module_name)
    version = getattr(module, "__version__", None)
    if version is None and distribution:
        version = package_version(distribution)
    location = getattr(module, "__file__", "built-in/unknown")
    return f"version={version or 'unknown'} | location={location}"


def gdal_report() -> str:
    from osgeo import gdal  # type: ignore

    return f"version={gdal.VersionInfo('RELEASE_NAME')} | python bindings imported"


def pyeo_endpoint_report() -> str:
    q = importlib.import_module("pyeo.queries_and_downloads")
    endpoint = getattr(q, "DATASPACE_API_ROOT", "<constant not found>")
    note = ""
    if "/resto/api/" in endpoint:
        note = " | WARNING: retired CDSE OpenSearch/RESTO endpoint detected"
    elif "/odata/v1/Products" in endpoint:
        note = " | OData catalogue endpoint detected"
    return endpoint + note


def command_report(command: str) -> str:
    found = shutil.which(command)
    return found or "not found on PATH"


def main() -> int:
    print("=" * 78)
    print("PyEO WINDOWS INSTALLATION VERIFICATION")
    print("=" * 78)
    print(f"Python executable : {sys.executable}")
    print(f"Python version    : {platform.python_version()}")
    print(f"Platform          : {platform.platform()}")
    print(f"Working directory : {os.getcwd()}")
    print(f"Conda prefix      : {os.environ.get('CONDA_PREFIX', '<not set>')}")
    print(f"Conda env name    : {os.environ.get('CONDA_DEFAULT_ENV', '<not set>')}")
    print(f"git command       : {command_report('git')}")
    print(f"jupyter command   : {command_report('jupyter')}")
    print("-" * 78)

    checks = [
        Check("PyEO package", lambda: import_report("pyeo", "pyeo")),
        Check("PyEO classification", lambda: import_report("pyeo.classification", "pyeo")),
        Check("PyEO data-access module", pyeo_endpoint_report),
        Check("GDAL", gdal_report),
        Check("NumPy", lambda: import_report("numpy", "numpy")),
        Check("Pandas", lambda: import_report("pandas", "pandas")),
        Check("GeoPandas", lambda: import_report("geopandas", "geopandas")),
        Check("Shapely", lambda: import_report("shapely", "shapely")),
        Check("scikit-learn", lambda: import_report("sklearn", "scikit-learn")),
        Check("scikit-image", lambda: import_report("skimage", "scikit-image")),
        Check("SciPy", lambda: import_report("scipy", "scipy")),
        Check("Sentinel Hub package", lambda: import_report("sentinelhub", "sentinelhub")),
        Check("Requests", lambda: import_report("requests", "requests")),
        Check("JupyterLab", lambda: import_report("jupyterlab", "jupyterlab"), required=False),
    ]

    failures = 0
    for check in checks:
        try:
            message = check.action()
            print(f"[PASS] {check.name}: {message}")
        except Exception as exc:  # diagnostic utility: report all failures
            marker = "FAIL" if check.required else "WARN"
            print(f"[{marker}] {check.name}: {type(exc).__name__}: {exc}")
            if check.required:
                failures += 1

    print("-" * 78)
    if os.environ.get("CONDA_DEFAULT_ENV") != "pyeo_env":
        print("[WARN] The active Conda environment is not named 'pyeo_env'.")
        print("       Run: conda activate pyeo_env")

    if failures:
        print(f"RESULT: FAILED — {failures} required check(s) did not pass.")
        return 1

    print("RESULT: CORE INSTALLATION CHECKS PASSED.")
    print("NOTE: A retired /resto/api/ endpoint warning is a data-access compatibility")
    print("      issue, not an installation failure. Follow the workflow's CDSE gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
