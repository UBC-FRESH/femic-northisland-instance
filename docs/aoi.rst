North Island AOI
================

The model AOI comes from the Basecamp FRST 558 email thread, "North Island
Timber Supply Area", received on 2026-10-21. The sender defined the area as the
portion of the North Island TSA inside the North Island - Central Coast Natural
Resource District, with the community forest agreement added back.

Operational rule
----------------

1. Select TSA 48 from ``WHSE_ADMIN_BOUNDARIES.FADM_TSA``.
2. Clip it to the Natural Resource District where ``ORG_UNIT = 'DNI'``.
3. Union the active community forest agreement polygons that touch the result.

The tracked artifact is ``data/source/aoi/northisland_aoi.gpkg``. Its layer is
``northisland_aoi``, its CRS is EPSG:3005, and its reviewed area is
1,083,003.66 ha.

Build command
-------------

.. code-block:: bash

   python scripts/build_aoi.py --out data/source/aoi/northisland_aoi.gpkg

The script fetches the public ArcGIS REST layers, writes the GeoPackage, and
writes a JSON summary beside it. The summary is the review checkpoint for the
area, bounds, and community forest count.

Review points
-------------

The email says "add back in the CFA" without naming the file. The public tenure
layer returns only K3Z, the North Island Community Forest, as an active
community forest touching the clipped TSA. The script unions that file into the
boundary. Confirm the file against the attached map before release.

The 2020 TSR data package and the 2024 determination PDF are context documents.
They are not geometry inputs.
