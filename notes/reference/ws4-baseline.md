# ws4 baseline and web UI

The baseline is a clearcut-at-age-60 replay. It is a smoke and teaching run for
the web UI, not an optimized or policy-ready schedule. The v0.2.0 base model
also applies the retention decision in `notes/reference/retention-decision.md`.

## Baseline

- Schedule: 46,321 blocks, target age 60, treatment `CC`.
- Retained AUs: `CWH_CW_L` and `CWH_YC_L`.
- Retained blocks: 4,968; retained total stand area: 52,013.6 ha; retained
  model THLB: 1,717.6 ha.
- Horizon: 100 years.
- Run: `runtime/baseline`.
- Product totals by decade (m3, rounded):

| Decade | Harvested volume |
| --- | ---: |
| 0-9 | 10,384,983 |
| 10-19 | 2,428,084 |
| 20-29 | 4,378,107 |
| 30-39 | 164,080 |
| 40-99 | 0 |

The front-loaded cut is the expected result of harvesting every eligible block
that is already at or beyond age 60 in period zero.

The 100-year managed volume is 17,355,255 m3, or 173,553 m3/yr. The pro-rated
AAC is 176,330 m3/yr; the baseline carries 98.4% of it.

## Targets

`config/targets.yaml` holds two provisional targets:

| Account | Period | Minimum | Realized | Status |
| --- | ---: | ---: | ---: | --- |
| `product.Yield.managed.Total` | 1 | 1,000,000 | 10,384,982.97 | met |
| `feature.Yield.managed.Total` | 5 | 5,000,000 | 6,796,794.26 | met |

Period 1 covers years 0-9 and period 5 covers years 40-49 on the offset clock.
These are smoke targets, not the AAC. The pro-rated AAC comparison is in
`notes/reference/retention-decision.md`.

## Web UI

Command:

```bash
./serve_northisland.sh
```

The launcher binds `127.0.0.1:8014`, passes `--crs EPSG:3005`, and sets the agent
working directory to the instance root.

Verification:

- `/health` returns `{"status":"ok"}`.
- The run list contains `baseline (simulate)`.
- The map renders the AOI blocks; the retained AUs remain in the view but are
  absent from the treatment schedule.
- The Targets tab shows both provisional targets with `met` status and their
  realized values.
- The map uses exact block geometry and the NICC land-base underlay. If WebGL
  is unavailable, the **SVG (fallback)** map engine renders the same blocks.

## Related dataset

The full TSA 48 benchmark is a separate instance in
`UBC-FRESH/femic-tsa48-instance`. It provides the NICC share reference and is
not required to run this model. See `notes/reference/related-instances.md`.
