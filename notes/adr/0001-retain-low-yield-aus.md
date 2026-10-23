# ADR 0001: Retain the two lowest-yield AUs in the NICC base model

Status: accepted
Date: 2026-10-23
Issues: #34, #35

## Context

The accepted managed curves use public RESULTS species/density with the model
PSPL/VDYP site index. Eight of twelve AUs meet or beat VDYP on gross volume over
ages 60-120. Four AUs remain below:

- CWH_HW_L: 0.89 gross
- CWH_CW_L: 0.46 gross
- CWH_CW_M: 0.80 gross
- CWH_YC_L: 0.71 gross

The four AUs are productive enough to hold old first-growth stock, but the
second-growth TIPSY curves are weak relative to VDYP. Retaining all four would
remove 32.0% of model THLB and reduce the 100-year average managed harvest from
176,955 to 139,825 m3/yr, or 79.3% of the pro-rated AAC. That is too large a
loss for a base model that is meant to support later optimization.

## Decision

Retain CWH_CW_L and CWH_YC_L at 100% and remove their blocks from the harvest
schedule. Keep harvesting CWH_HW_L and CWH_CW_M, even though their managed
curves are slightly below VDYP, because they carry most of the volume among
the four problem AUs.

The policy is recorded in `config/retention.json` and applied by
`scripts/build_baseline_schedule.py --retention-config`.

## Consequences

- Model THLB falls from 28,557.9 to 26,840.3 ha, a 6.0% reduction.
- The 100-year average managed harvest falls from 176,955 to 173,553 m3/yr.
- That is 98.4% of the 176,330 m3/yr pro-rated AAC, so the base model still
  carries the intended harvest level.
- The two retained AUs remain in the dataset with their VDYP curves. Their
  managed TIPSY curves are not scheduled and are not used by the baseline.
- The base model is not a formal sustained-yield AAC calculation. It is a
  deterministic one-pass baseline that preserves a credible land base and
  harvest level for later optimization.

## Alternatives considered

- **Retain all four.** Rejected: 32.0% THLB loss and 79.3% of pro-rated AAC.
- **Retain CWH_HW_L and CWH_CW_M.** Rejected: 26.0% THLB loss and 81.2% of
  pro-rated AAC; these AUs carry most of the volume.
- **Retain none.** Rejected: continues to schedule second-growth on the two
  worst low-yield AUs and weakens the teaching rationale.
- **Delete the managed TIPSY curves for the retained AUs from the bundle.**
  Deferred: the curves are retained as provenance and are not used by the
  baseline. A later bundle cleanup can remove them without changing the
  schedule.
