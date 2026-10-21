# ws4 build evidence

The downstream FreshForge workflow compiles the FEMIC XML/fragments export into
the canonical ws4 matrix.

## Command

```bash
python -m freshforge run workflows/freshforge/northisland_ws4_from_bundle.yaml \
  --workdir runtime/freshforge \
  --namespace northisland/ws4 \
  --json
```

## Source export

```text
patchworks export completed tsa=['northisland'] au=12 fragments=51289 curves=49
forestmodel.xml and fragments.shp written under output/patchworks_northisland/
```

## Dataset

| Table | Rows |
| --- | --- |
| fragments | 56,187 |
| blocks | 56,187 |
| tracks | 9,612 |
| curves | 2,156 |
| treatments | 5,930 |
| products | 17,790 |
| features | 57,672 |
| accounts | 33 |

`ws4.cli validate` returns `Dataset is valid`. The manifest records the
`forestmodel.xml` and `fragments.shp` SHA-256 digests.

## Coverage

| Check | Value |
| --- | --- |
| Block area | 442,451.9975 ha |
| Managed area at year 0 | 285,579.4582 ha |
| Unmanaged area at year 0 | 413,894.0517 ha |
| Baseline schedule blocks | 51,289 |
| Baseline horizon | 100 years |

The managed/unmanaged split comes from the FEMIC retention/IFM export. The
baseline schedule deduplicates split block portions, so it has fewer rows than
the blocks table.
