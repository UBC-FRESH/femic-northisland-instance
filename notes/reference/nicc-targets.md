# NICC reference harvest targets

Status: reference floor set from the full-TSA benchmark; not a formal AAC determination.

## Reference

The full TSA 48 benchmark gives the NICC part these values:

- first-decade harvest: 2,145,437 m3
- first-decade NICC share: 17.19%
- scaled AAC reference: **214,544 m3/yr**

That is a share of the published full-TSA AAC, not an independent NICC AAC. The
full-model NICC part and the standalone NICC model have different land bases, so
the target is a planning reference until reviewed.

## Target set

`config/targets.yaml` now carries:

- a **2,145,437 m3 floor for each of the ten decades** (214,544 m3/yr);
- the existing 5,000,000 m3 growing-stock smoke target at period 5.

The floor is a sustained-yield reference, not a ceiling. The opening-size
ceilings are a separate policy and live in the MKRF/TSA 48 target sets.

The provisional two-target set is preserved as
`config/targets.provisional.yaml`.

## Verified run

`runtime/reference` is the 5,000-iteration search from the baseline schedule
(`runtime/target_reference_search_warm`) re-reported against the new targets.

| Decade | Managed harvest (m3) | Target floor | Status |
| --- | ---: | ---: | --- |
| 1 | 2,188,177 | 2,145,437 | met |
| 2 | 2,154,008 | 2,145,437 | met |
| 3 | 2,145,497 | 2,145,437 | met |
| 4 | 2,149,870 | 2,145,437 | met |
| 5 | 2,147,995 | 2,145,437 | met |
| 6 | 2,147,178 | 2,145,437 | met |
| 7 | 2,166,047 | 2,145,437 | met |
| 8 | 2,151,315 | 2,145,437 | met |
| 9 | 2,421,871 | 2,145,437 | met |
| 10 | 3,018,029 | 2,145,437 | met |
| **Total** | **22,689,987** | | |
| **Average** | **226,900 m3/yr** | 214,544 m3/yr | above floor |

The later decades exceed the floor; this is a floor target, not an even-flow
target. A formal AAC review would need a sustained-yield optimization and an
accepted yield/policy package.

## Caveat

Do not present 214,544 m3/yr as an NICC AAC. It is the full-TSA benchmark's
NICC-share reference. The standalone model's pro-rated AAC on its own THLB is
176,330 m3/yr; the difference is the land-base/curve scope.
