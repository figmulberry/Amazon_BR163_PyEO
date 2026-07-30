#!/usr/bin/env python
r"""Download one product returned by cdse_odata_probe.py.

This diagnostic script uses the current Copernicus Data Space identity service and
current download host. It never prints the access token or password.

Example (Miniconda Prompt):
    conda activate pyeo_env
    python cdse_download_one.py ^
      --catalog C:\GIS\projects\Amazon_BR163_PyEO\00_admin\cdse_probe.csv ^
      --credentials C:\GIS\secrets\pyeo_cdse.ini ^
      --row 0 ^
      --out-dir C:\GIS\data\Amazon_BR163_PyEO\test_download ^
      --extract
"""
from __future__ import annotations

import argparse
import configparser
import csv
import os
import re
import sys
import zipfile
from pathlib import Path
from typing import Dict, List

import requests

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/"
    "protocol/openid-connect/token"
)
DOWNLOAD_ROOT = "https://download.dataspace.copernicus.eu/odata/v1/Products"
UUID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def read_credentials(path: Path) -> tuple[str, str]:
    parser = configparser.ConfigParser()
    with path.open("r", encoding="utf-8-sig") as handle:
        parser.read_file(handle)
    try:
        username = parser.get("dataspace", "user").strip()
        password = parser.get("dataspace", "pass").strip()
    except (configparser.Error, KeyError) as exc:
        raise RuntimeError(
            "Credentials file must contain [dataspace], user=..., and pass=..."
        ) from exc
    placeholders = {"", "YOUR_CDSE_EMAIL", "YOUR_CDSE_PASSWORD", "replace_this"}
    if username in placeholders or password in placeholders:
        raise RuntimeError("Replace the template values with your CDSE credentials first")
    return username, password


def get_access_token(username: str, password: str) -> str:
    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": "cdse-public",
            "grant_type": "password",
            "username": username,
            "password": password,
        },
        timeout=90,
    )
    if response.status_code != 200:
        detail = response.text[:1000]
        raise RuntimeError(
            f"CDSE token request failed with HTTP {response.status_code}: {detail}"
        )
    payload = response.json()
    token = payload.get("access_token")
    if not token:
        raise RuntimeError("CDSE response did not contain access_token")
    return str(token)


def read_catalog_row(path: Path, row_index: int) -> Dict[str, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows: List[Dict[str, str]] = list(csv.DictReader(handle))
    if not rows:
        raise RuntimeError("Catalogue CSV contains no product rows")
    if row_index < 0 or row_index >= len(rows):
        raise RuntimeError(
            f"--row {row_index} is outside the available range 0 to {len(rows)-1}"
        )
    return rows[row_index]


def safe_product_filename(title: str, product_uuid: str) -> str:
    clean = title.strip() or product_uuid
    clean = re.sub(r"[<>:\\|?*\"]", "_", clean)
    clean = clean.rstrip(". ")
    if clean.lower().endswith(".zip"):
        return clean
    return clean + ".zip"


def download_product(product_uuid: str, token: str, destination: Path) -> None:
    url = f"{DOWNLOAD_ROOT}({product_uuid})/$value"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "PyEO-BR163-workflow/1.0",
    }
    with requests.get(url, headers=headers, stream=True, timeout=(60, 900)) as response:
        if response.status_code != 200:
            detail = response.text[:1200]
            raise RuntimeError(
                f"Product download failed with HTTP {response.status_code}: {detail}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        total_header = response.headers.get("Content-Length")
        total_bytes = int(total_header) if total_header and total_header.isdigit() else None
        written = 0
        next_report = 100 * 1024 * 1024
        part_path = destination.with_suffix(destination.suffix + ".part")
        try:
            with part_path.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    handle.write(chunk)
                    written += len(chunk)
                    if written >= next_report:
                        if total_bytes:
                            print(
                                f"Downloaded {written/1_000_000:.0f} MB of "
                                f"{total_bytes/1_000_000:.0f} MB"
                            )
                        else:
                            print(f"Downloaded {written/1_000_000:.0f} MB")
                        next_report += 100 * 1024 * 1024
            os.replace(part_path, destination)
        except Exception:
            if part_path.exists():
                part_path.unlink()
            raise
    print(f"Download complete: {destination}")
    print(f"File size: {destination.stat().st_size/1_000_000:.2f} MB")


def extract_zip(zip_path: Path, out_dir: Path) -> None:
    extract_dir = out_dir / zip_path.stem
    extract_dir.mkdir(parents=True, exist_ok=True)
    print(f"Testing ZIP integrity: {zip_path.name}")
    with zipfile.ZipFile(zip_path, "r") as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise RuntimeError(f"ZIP integrity test failed at member: {bad_member}")
        print(f"Extracting to: {extract_dir}")
        archive.extractall(extract_dir)
    safe_dirs = list(extract_dir.rglob("*.SAFE"))
    print(f"SAFE directories found after extraction: {len(safe_dirs)}")
    for safe_dir in safe_dirs[:5]:
        print(f"  {safe_dir}")
    if not safe_dirs:
        print("WARNING: No .SAFE directory was found. Inspect the extracted contents.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, help="CSV from cdse_odata_probe.py")
    parser.add_argument("--credentials", required=True, help="INI with [dataspace] credentials")
    parser.add_argument("--row", type=int, default=0, help="Zero-based CSV row to download")
    parser.add_argument("--out-dir", required=True, help="Destination folder")
    parser.add_argument("--extract", action="store_true", help="Test and extract the ZIP")
    args = parser.parse_args()

    catalog = Path(args.catalog)
    credentials = Path(args.credentials)
    out_dir = Path(args.out_dir)
    if not catalog.exists():
        parser.error(f"Catalogue CSV does not exist: {catalog}")
    if not credentials.exists():
        parser.error(f"Credentials file does not exist: {credentials}")

    row = read_catalog_row(catalog, args.row)
    product_uuid = (row.get("uuid") or "").strip()
    title = (row.get("title") or product_uuid).strip()
    if not UUID_PATTERN.match(product_uuid):
        raise RuntimeError(f"Catalogue row does not contain a valid product UUID: {product_uuid}")

    print("Selected product")
    print(f"  Row   : {args.row}")
    print(f"  Name  : {title}")
    print(f"  UUID  : {product_uuid}")
    print("Requesting a CDSE token (token value will not be displayed)...")
    username, password = read_credentials(credentials)
    token = get_access_token(username, password)
    print("Token request: PASS")

    output_zip = out_dir / safe_product_filename(title, product_uuid)
    download_product(product_uuid, token, output_zip)
    if args.extract:
        extract_zip(output_zip, out_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Cancelled by user.", file=sys.stderr)
        raise SystemExit(130)
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
