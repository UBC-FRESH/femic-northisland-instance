Web UI
======

The ws4 web UI serves a compiled dataset and its runs. It is read-only except for
the optional run and agent controls. It binds loopback by default and has no
authentication.

Launch
------

.. code-block:: bash

   python -m ws4.cli serve \
     --dataset runtime/matrix \
     --runs runtime \
     --geometry runtime/fragments.geojson \
     --land-base runtime/land_base.geojson \
     --targets config/targets.yaml \
     --crs EPSG:3005 \
     --allow-runs \
     --allow-agent \
     --port 8014

Generate the land-base underlay once after the matrix build:

.. code-block:: bash

   python scripts/prepare_land_base.py \
     --aoi data/source/aoi/northisland_aoi.gpkg \
     --out runtime/land_base.geojson

The North Island geometry is EPSG:3005. Pass ``--crs EPSG:3005`` so the server
can project it for MapLibre, which renders in WGS84. The land base is the AOI
polygon drawn under the blocks, so non-forest gaps read as land rather than as
missing data. The block layer still renders if the OpenStreetMap basemap tiles
are unavailable.

The North Island map contains 51,289 compiled block polygons. ``prepare_ws4_ui.py``
keeps every source vertex (``--simplify-m 0``); the uncompressed response is
about 61 MB and the ws4 gzip middleware compresses it in transit. If MapLibre
cannot create a WebGL context, switch **Map engine** to **SVG (fallback)**.

In the v0.2.0 base model, ``CWH_CW_L`` and ``CWH_YC_L`` are retained. Their
blocks remain visible in the map but are absent from the harvest schedule. The
baseline schedule has 46,321 blocks and the remaining model THLB is 26,840.3 ha.

Checks
------

- ``/health`` returns ``{"status":"ok"}``.
- The map shows the AOI blocks, not a world view.
- The run list contains the baseline run.
- The target table shows the configured targets and their realized values.
- The UI can switch runs without a server restart.

The v0.2.0 smoke renders 51,289 blocks, applies the retention schedule, and
displays both provisional targets as `met`. See
``notes/reference/ws4-baseline.md`` and :doc:`retention-policy`.

Do not use ``--allow-remote`` on an untrusted network. Put the service behind a
trusted proxy if it must be reachable from another host.
