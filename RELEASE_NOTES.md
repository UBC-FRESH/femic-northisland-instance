# FEMIC North Island Instance v0.2.0

Released 2026-10-23.

This release locks the North Island NICC base model. It adds the public RESULTS
managed-curve lane, the Linux + Wine BatchTIPSY lane, the retention policy, and
the rebuilt baseline and web UI.

## Highlights

- Managed curves use public RESULTS species and density with the model
  PSPL/VDYP site index.
- BatchTIPSY runs under Wine on Linux through the scratch-prefix and userspace
  Xvfb recipe in `runbooks/tipsy-btc-linux-wine.md`.
- The baseline retains `CWH_CW_L` and `CWH_YC_L` and keeps `CWH_HW_L` and
  `CWH_CW_M` harvestable.
- The retained AUs remove 1,717.6 ha, or 6.0%, of model THLB. The 100-year
  average managed harvest is 173,553 m3/yr, or 98.4% of the 176,330 m3/yr
  pro-rated AAC.
- The ws4 dataset validates, both provisional targets are met, and the UI serves
  the rebuilt baseline.

## Evidence

- `docs/retention-policy.rst`
- `notes/reference/retention-decision.md`
- `notes/adr/0001-retain-low-yield-aus.md`
- `config/tsr/tipsy_au_results_vdyp_comparison.csv`
- `config/tsr/thlb_area_by_au.csv`
- `config/retention.json`

## Compatibility

- The 12 model AU keys and the AOI are unchanged.
- Set `retain_aus` to an empty list in `config/retention.json` to rebuild the
  harvest-all-AUs baseline.
- The retained AUs keep their VDYP curves in the bundle. Their managed TIPSY
  curves are not scheduled.
