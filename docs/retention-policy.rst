Retention Policy and the v0.2.0 Base Model
==========================================

Purpose
-------

This page records the process, analysis, rationale, and decision behind the
retention policy in the v0.2.0 North Island base model. It is the public
explanation for why two of the four low-yield AUs are retained and the other two
remain in the harvest schedule.

The machine-readable policy is ``config/retention.json``. The decision record is
``notes/adr/0001-retain-low-yield-aus.md``. The full working note is
``notes/reference/retention-decision.md``.

Starting point
--------------

The accepted managed curves use public RESULTS species and density with the
model PSPL/VDYP site index. The TSA 48 OAF 1 of 15% is applied, and OAF 2 is 5%
except for CWH_FD, where it is 12.5%. Eight of twelve AUs meet or beat VDYP on
gross volume over ages 60, 80, 100, and 120. Four remain below:

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 18 22

   * - AU
     - Gross TIPSY / VDYP
     - Merchantable / VDYP
     - Model THLB (ha)
     - Reading
   * - CWH_HW_L
     - 0.89
     - 0.70
     - 4,312.6
     - below, but carries material volume
   * - CWH_CW_M
     - 0.80
     - 0.65
     - 3,112.0
     - below, but carries material volume
   * - CWH_CW_L
     - 0.46
     - 0.23
     - 1,497.2
     - weakest curve, negligible volume
   * - CWH_YC_L
     - 0.71
     - 0.27
     - 220.4
     - weakest curve, negligible volume

The ratios are means over ages 60-120. CWH_HW_L crosses above VDYP on gross
volume at later ages, but its 60-120 mean remains below 1.0.

Question
--------

Should the base model continue to schedule second-growth harvest in these four
AUs? If not, which ones should be retained, and what happens to THLB and the
pro-rated AAC?

Method
------

The base dataset was compiled with the accepted managed curves. For each
retention scenario, blocks whose feature labels place them in the selected AU
were removed from the deterministic clearcut-at-age-60 schedule. Retained stands
remain in the dataset with their VDYP curves. The simulation horizon was 100
years.

This is a schedule-level scenario, not a formal sustained-yield optimization.
The pro-rated AAC is the 2024 TSA 48 AAC of 1,096,000 m3/yr scaled by the model
THLB share of the TSR current THLB of 177,505 ha:

.. code-block:: text

   1,096,000 * 28,557.9 / 177,505 = 176,330 m3/yr

Scenario results
----------------

.. list-table::
   :header-rows: 1
   :widths: 32 17 17 20 20

   * - Scenario
     - THLB remaining
     - Retained THLB
     - 100-yr average
     - Share of pro-rated AAC
   * - Harvest all AUs
     - 28,557.9 ha
     - 0.0 ha
     - 176,955 m3/yr
     - 100.4%
   * - Retain CWH_CW_L + CWH_YC_L
     - 26,840.3 ha
     - 1,717.6 ha
     - 173,553 m3/yr
     - **98.4%**
   * - Retain CWH_HW_L + CWH_CW_M
     - 21,133.3 ha
     - 7,424.6 ha
     - 143,228 m3/yr
     - 81.2%
   * - Retain all four
     - 19,415.7 ha
     - 9,142.2 ha
     - 139,825 m3/yr
     - 79.3%

The first 10-year period is dominated by old-growth liquidation. In the
accepted two-AU retention scenario it is 10,384,983 m3, or about 1.038M m3/yr.
That is above the pro-rated AAC and is not the long-run comparison. The 100-year
average is the stable comparison because the baseline schedule harvests every
eligible block once and then stops.

Decision
--------

Retain **CWH_CW_L** and **CWH_YC_L**, and keep harvesting **CWH_HW_L** and
**CWH_CW_M**.

The two retained AUs are the ones where the managed curve is clearly weak and
the long-run volume contribution is negligible. Retaining them removes only
1,717.6 ha, or 6.0% of model THLB, and keeps the 100-year average at 98.4% of
the pro-rated AAC. Retaining the other two as well would remove 32.0% of THLB
and drop the average to 79.3% of the pro-rated AAC, which is too large a loss
for a base model that is meant to support later optimization.

Implementation
--------------

The policy is stored in ``config/retention.json`` and applied by the baseline
schedule builder:

.. code-block:: bash

   python scripts/build_baseline_schedule.py \
     --dataset runtime/matrix \
     --out runtime/baseline_schedule.csv \
     --target-age 60 \
     --retention-config config/retention.json

The FreshForge ``build_baseline_schedule`` node passes
``retention_config: config/retention.json`` in both
``workflows/freshforge/northisland_model_build.yaml`` and
``workflows/freshforge/northisland_ws4_from_bundle.yaml``. The accepted
baseline is written to ``runtime/baseline`` and served by the ws4 UI.

Accepted baseline
-----------------

.. list-table::
   :header-rows: 0
   :widths: 50 50

   * - Scheduled blocks
     - 46,321
   * - Scheduled area
     - 390,438.4 ha
   * - Retained blocks
     - 4,968
   * - Retained total stand area
     - 52,013.6 ha
   * - Retained model THLB
     - 1,717.6 ha
   * - Remaining model THLB
     - 26,840.3 ha
   * - First decade managed volume
     - 10,384,983 m3
   * - 100-year managed volume
     - 17,355,255 m3
   * - 100-year average
     - 173,553 m3/yr
   * - Pro-rated AAC
     - 176,330 m3/yr
   * - Share of pro-rated AAC
     - 98.4%
   * - Provisional targets
     - both met

Rationale
---------

The decision separates the two ideas that were being mixed together:

1. The **stand-level** question is whether second-growth management is
   defensible on a low-productivity AU. For CWH_CW_L and CWH_YC_L it is not:
   the managed curves are far below VDYP and the volume contribution is
   negligible.
2. The **land-base** question is whether removing an AU breaks the harvest
   level. Removing all four does; removing only the two weakest does not.

The two retained AUs are a small part of the THLB and a negligible part of the
long-run volume. The two kept AUs are below VDYP but carry most of the volume
among the four, so retiring them would be expensive. Keeping them preserves the
base model's harvest level while the low-yield sites are removed from the
managed land base.

Risks and limitations
---------------------

- The retained AUs still contain old first-growth volume. Retaining them forgoes
  that near-term volume; the base model does not attempt to liquidate it.
- The pro-rated AAC uses the model THLB share of the TSR THLB. The model THLB
  flag is narrower than the TSR benchmark, so the ratio is an approximation.
- The baseline is a one-pass schedule. A sustained-yield optimization is still
  required before the value can be treated as a policy AAC.
- The managed TIPSY curves for the retained AUs remain in the bundle as
  provenance. They are not scheduled and do not contribute to the baseline.
  A later bundle cleanup can remove them without changing the schedule.
- The four-AU and two-AU results depend on the current RESULTS species/density
  and the PSPL/VDYP site-index mapping. Revisit the decision if either changes.

Evidence
--------

- ``config/tsr/tipsy_au_results_vdyp_comparison.csv``: AU-wise managed/VDYP
  ratios.
- ``config/tsr/thlb_area_by_au.csv``: model THLB and total stand area by AU.
- ``config/retention.json``: accepted policy and scenario numbers.
- ``notes/reference/retention-decision.md``: working analysis.
- ``notes/adr/0001-retain-low-yield-aus.md``: decision record.
- ``runtime/scenario_retain_cwlyc/run/report_targets.csv``: scenario target
  readout.
