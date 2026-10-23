Model Build
===========

The model build is a FreshForge workflow. Each node calls a recorded command and
names the artifact it writes. The workflow lives at
``workflows/freshforge/northisland_model_build.yaml``.

Chain
-----

.. code-block:: text

   femic.validate_case
     -> femic.geospatial_preflight
     -> femic.compile_upstream
     -> northisland.ws4.post_tipsy
     -> femic.export_patchworks
     -> northisland.ws4.build_dataset
     -> northisland.ws4.validate_dataset
     -> northisland.ws4.build_baseline_schedule
        (retention_config: config/retention.json)
     -> northisland.ws4.simulate
     -> northisland.ws4.report
     -> northisland.ws4.prepare_ui

FEMIC compiles the public inventory and yield curves and writes the model-input
bundle. The export reads the final checkpoint (`checkpoint8`) so the fragments
carry the full AOI. The Patchworks export gives ws4 a ForestModel XML recipe and a
fragment inventory. ws4 compiles the canonical matrix and runs the baseline
simulation.

The accepted North Island run produces 12 AUs across CWH_HW, CWH_CW, CWH_YC,
and CWH_FD. The managed lane uses public RESULTS species/density with the model
PSPL/VDYP site index and the TSA 48 OAF rules. The baseline applies the
retention policy in :doc:`retention-policy`: ``CWH_CW_L`` and ``CWH_YC_L`` are
retained, and the other ten AUs remain harvestable.

Commands
--------

.. code-block:: bash

   python -m pip install -e .
   python -m freshforge validate workflows/freshforge/northisland_model_build.yaml
   python -m freshforge plan workflows/freshforge/northisland_model_build.yaml
   export FEMIC_EXTERNAL_DATA_ROOT=/path/to/femic-public-data/data
   python -m freshforge run workflows/freshforge/northisland_model_build.yaml \
     --workdir runtime/freshforge \
     --namespace northisland/model-build \
     --json

The run writes the generated dataset, baseline run, report, and UI geometry under
``runtime/``. Those paths are ignored. The workflow document and the provider
commands are tracked.

Runtime boundary
----------------

VDYP7 is a Windows executable. On Linux it runs under Wine, including the 32-bit
loader. The first lane sets ``vdyp_sampling_mode: auto`` because the larger
``all`` batches exceeded the short VDYP console timeout in the first run. Auto
sampling fits from fewer stands, so it is a provisional workaround; raise the
timeout and rerun in ``all`` mode before release.

The accepted lane uses real BatchTIPSY managed curves. On Linux, BatchTIPSY runs
through the scratch Wine prefix, Wine Mono, and userspace Xvfb recipe in
``runbooks/tipsy-btc-linux-wine.md``. The managed curves are compared with VDYP
in ``notes/reference/tipsy-vs-vdyp.md`` and ``docs/retention-policy.rst``.
