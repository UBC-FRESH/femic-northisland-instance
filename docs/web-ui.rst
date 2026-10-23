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

The North Island geometry is EPSG:3005. Pass ``--crs EPSG:3005`` so the server
can project it for MapLibre, which renders in WGS84. The land base is the AOI
polygon drawn under the blocks, so non-forest gaps read as land rather than as
missing data. The block layer still renders if the OpenStreetMap basemap tiles
are unavailable.

The first North Island map contains 51,289 polygons. ``prepare_ws4_ui.py`` now
keeps every source vertex (``--simplify-m 0``); the uncompressed response is
about 61 MB and the ws4 gzip middleware compresses it in transit. If MapLibre
cannot create a WebGL context, switch **Map engine** to **SVG (fallback)**.

Checks
------

- ``/health`` returns ``{"status":"ok"}``.
- The map shows the AOI blocks, not a world view.
- The run list contains the baseline run.
- The target table shows the configured targets and their realized values.
- The UI can switch runs without a server restart.

The first North Island smoke rendered 51,289 blocks, showed 4,746 treated in
period 2, and displayed both provisional targets as `met`. See
``notes/reference/ws4-baseline.md``.

Do not use ``--allow-remote`` on an untrusted network. Put the service behind a
trusted proxy if it must be reachable from another host.
