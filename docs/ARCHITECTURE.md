# Workbook-backed architecture

`domain.py` contains the unchanged canonical Project → Chemistry → Cell Size hierarchy and ten modules. `storage.py` keeps existing source/metadata storage, creates module roots and short relative symlinks for teams, and removes legacy child folders only when empty. Existing nonempty folders and immutable source bytes are preserved.

## Excel control records

`workbook_store.py` is the schema registry and persistence layer. Each functional item has exactly one `.xlsx` file in its module. Its child topics are sheets. Input schemas have typed fields, required IDs/PICs, bounded rows, approval values and unit/condition checks where required. Technical register columns come from the Information fields supplied in `docs/USER_REQUIREMENTS.tsv`; these text records do not silently drive electrochemical calculations.

- Live workbooks: `data/projects/<project>/<chemistry>/<size>/<module>/`.
- Example workbooks: `data/example_data/projects/...`, selected explicitly by dataset.
- Short team paths: `data/teams/...`, symlinks to live module roots.
- Earlier workbook versions and audit: `<dataset root>/workbook_history/<cell>/<book>/`.
- Per-cell file locks: `<dataset root>/workbook_locks/`.

Saving requires a SHA-256 revision. A cell-wide `flock` serializes application writers, a checksum detects stale edits, the prior workbook is preserved by digest, and a temporary file is flushed/fsynced then atomically replaced. Audit records time, actor, sheet and old/new digests. File history covers app writes, not every direct external edit. External Excel does not honor the app's lock; avoid editing the same workbook by both routes simultaneously. Existing unknown sheets/header changes are rejected to prevent destructive rewriting. Templates accept values, not Excel formulas or macros. Server-side calculations avoid stale cached formula values.

`example_project.py` seeds only missing files in the separate example dataset. Live files start empty. Neither startup nor UI polling reseeds existing workbooks. Example data is illustrative, including predicted cycle life and synthetic curves; no actual test evidence is claimed.

## Calculation and rendering

`live_data.py` reads persisted workbooks on each summary request. It computes weighted progress, milestones, budget, issue colors, condition-matched Approved capacity/energy, explicitly predicted life at matching EOL and separate Prototype/SOP costs. Null means unavailable, never a synthetic fallback. Multiple currencies or ambiguous measurement conditions prevent unsafe aggregation. The latest approved measurement date is selected; energy is total Wh / total kg, capacity is the mean of matching approved samples that day.

`app.py` exposes scoped workbook/sheet APIs, summary/task queries, XLSX downloads and a complete per-cell workbook ZIP. Dataset and workbook paths are allowlisted. Changes require JSON with a custom same-origin request header; no cross-origin CORS access is enabled. Optional environment credentials protect all routes with HTTP Basic; use HTTPS termination for shared hosting.

`static/app.js` uses flat sidebar groups including Cell Design, Materials, DOE, Manufacturing and Cell Analysis. Context/team selectors are in the content area. File and sheet selectors replace the old nested folder tree. The editor writes server files, supports tabular paste and displays conflicts without discarding inputs. The dashboard polls files every 30 seconds; if a file is invalid, it shows an explicit error/stale-data notice instead of treating old values as current. Downloads are copies and are not a synchronization agent.

## Original Cycler / Digital Twin

`integrations/digital_twin/` pins the original model from user-provided repo commit `1b999d16822729adfb4df463804af0f8906a0034`. `cycler_service.py` owns one lazily initialized rack and simulation worker. `static/twin_viewer.js` adapts the original Three.js rack, selection and uniform temperature coloring. The example project's prismatic view selects the six assigned channels; controls still affect all twelve original rack channels. Simulations are restricted to the example dataset and never write Approved workbook KPIs.

The second twin mode reads `Cell Mapping` and `Cell State` sheets. It renders parametric dimensions and recorded telemetry snapshots, not a live hardware connection or imported CAD. Timestamp/Cell ID links are validated. The viewer limits geometry to the first 100 mapped cells. Native STEP, a physical cycler adapter, calibrated chemistry/geometry physics and a spatial thermal field are not implemented.

`serve.py` uses one Waitress process with multiple threads. Do not use multiple WSGI processes: each would get a separate in-memory rack. Rack telemetry resets when the process restarts; persisted workbooks do not. The model's latched STOP is simulation logic, not independent hardware protection.

## Deployment boundary

The workbook workflow is operational locally. Public hosting, reverse proxy HTTPS, persistent volume and secure credential injection remain deployment tasks. HTTP Basic is a shared login; individual RBAC, independent approvals/signatures, malware scanning, external database connectors and automated raw measurement ingestion are not supplied. Deployment must back up the entire persistent data directory; code in Git is not a backup of working Excel files.
