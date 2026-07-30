#!/usr/bin/env python
r"""Query the current Copernicus Data Space OData catalogue for Sentinel-2 L2A.

This is a diagnostic companion for the PyEO workflow. It does not modify PyEO.
It uses the bounding box of a supplied ROI to keep the OData URL short, then writes
both the raw response and a compact CSV catalogue.

Example (Miniconda Prompt):
    conda activate pyeo_env
    python cdse_odata_probe.py ^
      --roi C:\GIS\projects\Amazon_BR163_PyEO\01_roi\pilot\amazon_br163_pilot.gpkg ^
      --start 2025-07-01 --end 2025-09-30 --cloud 25 --top 10 ^
      --output C:\GIS\projects\Amazon_BR163_PyEO\00_admin\cdse_probe.csv
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

import geopandas as gpd
import pandas as pd
import requests
from shapely import wkt

CATALOGUE_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"


def parse_ymd(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use YYYY-MM-DD, for example 2025-07-01") from exc


def iso_start(day: date) -> str:
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.000Z"
    )


def attribute_map(attributes: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    mapped: Dict[str, Any] = {}
    for attribute in attributes or []:
        name = attribute.get("Name")
        if not name:
            continue
        mapped[name] = attribute.get("Value")
    return mapped


def product_row(item: Dict[str, Any]) -> Dict[str, Any]:
    attrs = attribute_map(item.get("Attributes", []))
    content_date = item.get("ContentDate") or {}
    content_length = item.get("ContentLength")
    size_mb = None
    if isinstance(content_length, (int, float)):
        size_mb = round(float(content_length) / 1_000_000, 2)
    return {
        "uuid": item.get("Id"),
        "title": item.get("Name"),
        "start_date": content_date.get("Start"),
        "end_date": content_date.get("End"),
        "product_type": attrs.get("productType"),
        "processing_level": attrs.get("processingLevel"),
        "cloud_cover": attrs.get("cloudCover"),
        "relative_orbit_number": attrs.get("relativeOrbitNumber"),
        "platform_serial_identifier": attrs.get("platformSerialIdentifier"),
        "online": item.get("Online"),
        "content_length_mb": size_mb,
        "publication_date": item.get("PublicationDate"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roi", required=True, help="Polygon ROI file readable by GeoPandas")
    parser.add_argument("--start", required=True, type=parse_ymd, help="Inclusive start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, type=parse_ymd, help="Inclusive end date YYYY-MM-DD")
    parser.add_argument("--cloud", type=float, default=25.0, help="Maximum cloud cover percentage")
    parser.add_argument("--top", type=int, default=10, help="Maximum products to return (1-100)")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    if args.end < args.start:
        parser.error("--end must be on or after --start")
    if not 0 <= args.cloud <= 100:
        parser.error("--cloud must be between 0 and 100")
    if not 1 <= args.top <= 100:
        parser.error("--top must be between 1 and 100")

    roi_path = Path(args.roi)
    if not roi_path.exists():
        parser.error(f"ROI does not exist: {roi_path}")

    gdf = gpd.read_file(roi_path)
    if gdf.empty:
        raise RuntimeError("ROI layer contains no features")
    if gdf.crs is None:
        raise RuntimeError("ROI has no CRS. Define the correct CRS in QGIS before querying.")
    if not bool(gdf.geometry.is_valid.all()):
        raise RuntimeError("ROI contains invalid geometry. Run Fix Geometries in QGIS first.")

    gdf_4326 = gdf.to_crs(4326)
    query_geometry = gdf_4326.geometry.unary_union.envelope
    geometry_wkt = wkt.dumps(query_geometry, rounding_precision=8, trim=True)

    end_exclusive = args.end + timedelta(days=1)
    filter_parts = [
        "Collection/Name eq 'SENTINEL-2'",
        (
            "Attributes/OData.CSC.StringAttribute/any(att:"
            "att/Name eq 'productType' and "
            "att/OData.CSC.StringAttribute/Value eq 'S2MSI2A')"
        ),
        (
            "Attributes/OData.CSC.DoubleAttribute/any(att:"
            "att/Name eq 'cloudCover' and "
            f"att/OData.CSC.DoubleAttribute/Value le {args.cloud})"
        ),
        f"ContentDate/Start ge {iso_start(args.start)}",
        f"ContentDate/Start lt {iso_start(end_exclusive)}",
        f"OData.CSC.Intersects(area=geography'SRID=4326;{geometry_wkt}')",
    ]

    params = {
        "$filter": " and ".join(filter_parts),
        "$top": str(args.top),
        "$orderby": "ContentDate/Start asc",
        "$expand": "Attributes",
    }
    headers = {"User-Agent": "PyEO-BR163-workflow/1.0"}

    print("Querying current CDSE OData catalogue...")
    print(f"Catalogue: {CATALOGUE_URL}")
    print(f"ROI bounding box in EPSG:4326: {geometry_wkt}")
    response = requests.get(CATALOGUE_URL, params=params, headers=headers, timeout=120)
    print(f"HTTP status: {response.status_code}")
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print(response.text[:3000])
        raise

    payload = response.json()
    products = payload.get("value")
    if products is None:
        raise RuntimeError("The response does not contain the expected OData 'value' array")

    output_csv = Path(args.output)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_json = output_csv.with_suffix(".json")
    output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    rows = [product_row(item) for item in products]
    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output_csv, index=False)

    print(f"Products returned: {len(dataframe)}")
    print(f"CSV written: {output_csv}")
    print(f"Raw JSON written: {output_json}")
    if dataframe.empty:
        print("No matching products. Widen the dates or cloud threshold; do not guess.")
        return 2

    display_columns = [
        "title",
        "start_date",
        "cloud_cover",
        "relative_orbit_number",
        "content_length_mb",
    ]
    available = [column for column in display_columns if column in dataframe.columns]
    print(dataframe[available].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
