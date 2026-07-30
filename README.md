\# Amazon BR163 PyEO



Windows adaptation of the PyEO forest change detection workflow for monitoring forest clearing along the BR-163 corridor in the Brazilian Amazon.



\## Repository Structure



\- 00\_admin – configuration and reproducibility files

\- 00\_starting\_files – templates and helper scripts

\- 01\_roi – regions of interest

\- 02\_reference – administrative boundaries and Sentinel-2 reference layers

\- 03\_notebooks – operational Jupyter notebooks

\- 04\_training – training data

\- 05\_model – trained ExtraTrees model and evaluation outputs

\- 06\_composites – generated composites

\- 06\_outputs – generated raster outputs

\- 07\_classification – classification outputs

\- 08\_change – change detection outputs

\- 09\_qgis – optional QGIS project

\- 10\_exports – exported products

\- 11\_documentation – project documentation

\- 11\_logs – processing logs

\- 12\_reports – summary reports



\## Workflow



1\. Train the model.

2\. Build a cloud-free composite.

3\. Download monitoring imagery.

4\. Classify imagery.

5\. Detect forest change.

6\. Vectorise change polygons.

7\. Perform quality assurance.

