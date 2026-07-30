# PyEO / Copernicus Data Space compatibility note

Review date: 24 July 2026

The repository's Windows installation sequence remains useful for creating the
PyEO Conda environment and installing the package in editable mode.

The current main-branch data-access code still points its Sentinel-2 catalogue
query to the retired CDSE RESTO/OpenSearch endpoint and parses the old `features`
response structure. Copernicus Data Space decommissioned OpenSearch on 2 March
2026 and directs integrations to OData or STAC.

Therefore the master workflow separates four gates:

1. Install and import PyEO.
2. Prove the local processing stack using repository sample data.
3. Prove current CDSE OData query, authentication, and one L2A download using the
   diagnostic scripts in this companion package.
4. Update and regression-test PyEO's internal data-access path against the exact
   source commit recorded on the user's machine before enabling the automated
   pipeline.

The diagnostic OData scripts do not silently replace PyEO. They establish a known
good current-service baseline and the exact fields/download behaviour that the
PyEO integration must match.
