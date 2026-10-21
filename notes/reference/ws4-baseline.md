# ws4 baseline and web UI

The baseline is a clearcut-at-age-60 replay. It is a smoke run for the web UI,
not an optimized or policy-ready schedule.

## Baseline

- Schedule: 51,289 blocks, target age 60, treatment `CC`.
- Horizon: 100 years.
- Run: `runtime/baseline`.
- Product totals by decade (m3, rounded):

| Decade | Harvested volume |
| --- | ---: |
| 0-9 | 10,725,270 |
| 10-19 | 2,428,084 |
| 20-29 | 4,378,107 |
| 30-39 | 164,080 |

The front-loaded cut is the expected result of harvesting every block that is
already at or beyond age 60 in period zero.

## Targets

`config/targets.yaml` holds two provisional targets:

| Account | Period | Minimum | Realized | Status |
| --- | ---: | ---: | ---: | --- |
| `product.Yield.managed.Total` | 1 | 1,000,000 | 1,063,908.30 | met |
| `feature.Yield.managed.Total` | 5 | 5,000,000 | 6,885,994.52 | met |

Period 1 covers years 10-19 and period 5 covers years 50-59, with
`period_width: 10`.

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
- The map renders 51,289 blocks; 4,746 are treated in period 2 (years 10-19).
- The Targets tab shows both provisional targets with `met` status and their
  realized values.
- The browser console has no errors; the only messages are WebGL performance
  warnings from the headless renderer.
- The MapLibre basemap uses OpenStreetMap raster tiles.
