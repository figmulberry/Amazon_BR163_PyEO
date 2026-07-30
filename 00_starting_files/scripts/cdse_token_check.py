#!/usr/bin/env python
r"""Check CDSE credentials without printing the access token.

Example:
    conda activate pyeo_env
    python cdse_token_check.py --credentials C:\GIS\secrets\pyeo_cdse.ini
"""
from __future__ import annotations

import argparse
import configparser
from pathlib import Path

import requests

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/"
    "protocol/openid-connect/token"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--credentials", required=True)
    args = parser.parse_args()
    path = Path(args.credentials)
    if not path.exists():
        parser.error(f"Credentials file does not exist: {path}")

    config = configparser.ConfigParser()
    with path.open("r", encoding="utf-8-sig") as handle:
        config.read_file(handle)
    if not config.has_section("dataspace"):
        raise RuntimeError("Missing [dataspace] section")
    username = config.get("dataspace", "user", fallback="").strip()
    password = config.get("dataspace", "pass", fallback="").strip()
    if not username or not password or username.startswith("YOUR_") or password.startswith("YOUR_"):
        raise RuntimeError("Replace the credentials template values first")

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
        print(f"CDSE credential test: FAIL (HTTP {response.status_code})")
        print(response.text[:1200])
        return 1
    payload = response.json()
    if not payload.get("access_token"):
        print("CDSE credential test: FAIL (no access_token in response)")
        return 1
    print("CDSE credential test: PASS")
    print("Access token received but intentionally not displayed.")
    print(f"Token type: {payload.get('token_type', 'unknown')}")
    print(f"Expires in: {payload.get('expires_in', 'unknown')} seconds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
