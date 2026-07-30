PYEO ON WINDOWS — AMAZON BR-163 COMPANION FILES

1. Open the HTML workflow first. Do not run these files out of sequence.
2. Copy this entire folder to:
   C:\GIS\projects\Amazon_BR163_PyEO\00_starting_files
3. Never enter credentials inside a script or the cloned PyEO repository.
4. Copy templates\credentials_TEMPLATE.ini to:
   C:\GIS\secrets\pyeo_cdse.ini
   Then edit only the [dataspace] user and pass values.
5. Run scripts\verify_pyeo_installation.py only after activating pyeo_env.
6. Run scripts\cdse_odata_probe.py only after the pilot ROI is valid in QGIS.
7. Run scripts\cdse_download_one.py only after the probe CSV contains products.
8. The configuration template is intentionally disabled. Do not enable any
   do_* switch until the matching gate in the HTML workflow passes.
9. Do not commit SAFE products, GeoTIFFs, models, passwords, tokens, or logs to Git.
10. Keep the original clcr/pyeo remote as upstream and make compatibility changes
    only on a named branch in your fork.
