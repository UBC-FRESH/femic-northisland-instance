Release Notes
=============

v0.2.0 - North Island NICC base model
-------------------------------------

Released 2026-10-23.

This release turns the P5 TSR/TIPSY investigation into a locked base model. It
adds the public RESULTS managed-curve lane, the working Linux and Wine
BatchTIPSY recipe, the retention policy, and the rebuilt baseline and web UI.

Highlights
~~~~~~~~~~

- Public RESULTS species and density are combined with the model PSPL/VDYP site
  index for the managed curves.
- BatchTIPSY runs under Wine on Linux through the scratch-prefix and userspace
  Xvfb lane in ``runbooks/tipsy-btc-linux-wine.md``.
- The baseline retains ``CWH_CW_L`` and ``CWH_YC_L`` and keeps harvesting
  ``CWH_HW_L`` and ``CWH_CW_M``.
- The retained AUs remove 1,717.6 ha, or 6.0%, of model THLB. The 100-year
  average managed harvest is 173,553 m3/yr, or 98.4% of the 176,330 m3/yr
  pro-rated AAC.
- The ws4 dataset validates, both provisional targets are met, and the UI serves
  the rebuilt baseline.

Compatibility
~~~~~~~~~~~~~

- The model still uses the same 12 AU keys and the same AOI.
- The retention policy is additive: set ``retain_aus`` to an empty list to
  rebuild the harvest-all-AUs baseline.
- The retained AUs keep their VDYP curves in the bundle. Their managed TIPSY
  curves are not scheduled.

Evidence
~~~~~~~~

- ``notes/reference/retention-decision.md``
- ``notes/adr/0001-retain-low-yield-aus.md``
- ``docs/retention-policy.rst``
- ``config/tsr/tipsy_au_results_vdyp_comparison.csv``
- ``config/tsr/thlb_area_by_au.csv``
- ``config/retention.json``
