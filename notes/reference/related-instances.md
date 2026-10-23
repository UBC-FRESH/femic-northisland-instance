# Related North Island instances

The NICC and TSA 48 models are **deliberately related but independent**.

| Repository | Boundary | Primary use |
| --- | --- | --- |
| `UBC-FRESH/femic-northisland-instance` (this repo) | TSA 48 ∩ NICC + K3Z | NICC/MSFM planning, NICF expansion |
| `UBC-FRESH/femic-tsa48-instance` | full TSA 48 | AAC/THLB benchmark, part accounting, NICC-share reference |

## Shared inputs, separate runtimes

Both instances consume the same public BC inventory and FEMIC/VDYP export lane.
They do **not** share a compiled matrix, a run directory, or a web service.

- This model uses the NICC + K3Z boundary directly.
- The full model carries `part = nicc` / `part = outside` and `k3z` block flags.
- The full model's first-decade NICC harvest is the current reference for NICC
  target calibration: **≈214,544 m3/yr** (17.19% of the full AAC).

## Use them together or separately

Use this repository alone when the question is:

- what does the NICC/K3Z planning model produce at district scale?
- how does the proposed 8,000 ha NICF expansion change the NICC estate?
- what targets and scenarios does the student/MSFM lane need?

Use `femic-tsa48-instance` alone when the question is:

- can the full TSA 48 land base sustain the published AAC?
- how should the AAC be split between NICC and the rest of the TSA?
- what is the defensible NICC harvest reference?

Neither repository imports the other. A change in one is not automatically a
change in the other; record any shared assumption in both notes.
