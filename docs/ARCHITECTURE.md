# Data architecture

`domain.py` is the canonical hierarchy: projects and chemistry IDs are distinct; cell IDs combine project, chemistry and size. Modules are instantiated for each configured cell without flattening. The five current cells are CYL-LFP-40135, CYL-LFP-21700, CYL-SIB-40135, CYL-SIB-21700, PRI-LFP01-52148117.

`storage.py` initializes filesystem navigation folders and a SQLite document registry. Raw bytes are addressed by SHA-256, created exclusively, deduplicated and never updated through the application. Document metadata records a source digest, cell scope, module, folder, original filename, PIC, revision, DOE ID, build lot ID, sample cell ID and UTC submission timestamp. A unique constraint rejects a repeated filename/revision within a selected folder. Different revisions are separate records, even when they share the same source bytes. Reference JSON files provide human-readable navigation without duplicating sources.

`app.py` exposes hierarchy, scoped records, source download, intake, CSV export and ephemeral file preview. User submissions and synthetic demonstration records are combined for display but identified separately. Frontend text is escaped. File downloads use attachment disposition; no user path is accepted for storage lookup. Uploads are size-limited and extension-checked, but not malware-scanned. The app is for trusted local use only.

`static/app.js` handles navigation, Plotly interaction, intake and previews. Each cell sees only its own submissions. All KPI and chart values are synthetic constants and do not change based on uploads.

## Production evolution

Move source objects into versioned object storage and metadata to PostgreSQL. Add a source table keyed by digest and document-to-source relationships; replace prototype JSON references with a transactional projection. Enforce source immutability through storage policy and verify checksums at retrieval. Add authenticated team/PIC roles and approval transitions with append-only audit events. A queue should process uploads, scan files, and derive normalized engineering data under versioned processing definitions. Separate observed metrics, units, provenance, test conditions and uncertainty from KPI targets.

Connectors should register original source locations and version identities, not duplicate files across modules. Change watchers can enqueue idempotent processing keyed by source digest; preserve earlier raw versions. Cycler adapters map channels to Cell ID, DOE ID and Build Lot ID, with validation of sample identity and units before publishing calculated metrics. Backend connectors, change watchers and engineering calculations are not implemented in this prototype.

STEP ingestion requires a CAD conversion worker (for example OpenCascade) to create a web-viewable mesh and preserve the original STEP, units and revision association. The current Plotly cylinder is synthetic and not an imported model. CSV/XLSX/PDF preview is read-only; PDF preview extracts text, not a page rendering.

Publication and restoration must retain the complete `data/` directory. Running Python processes do not survive environment snapshot restoration. No fresh-task restoration has been verified.
