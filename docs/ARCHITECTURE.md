# Data architecture

`domain.py` is the canonical hierarchy: projects and chemistry IDs are distinct; cell IDs combine project, chemistry and size. Modules are instantiated for each configured cell without flattening. The five current cells are CYL-LFP-40135, CYL-LFP-21700, CYL-SIB-40135, CYL-SIB-21700, PRI-LFP01-52148117.

`storage.py` initializes filesystem navigation folders and a SQLite document registry. Raw bytes are addressed by SHA-256, created exclusively, deduplicated and never updated through the application. Document metadata records a source digest, cell scope, module, folder, original filename, PIC, revision, DOE ID, build lot ID, sample cell ID and UTC submission timestamp. A unique constraint rejects a repeated filename/revision within a selected folder. Different revisions are separate records, even when they share the same source bytes. Reference JSON files provide human-readable navigation without duplicating sources.

`app.py` exposes hierarchy, scoped records, source download, intake, CSV export and ephemeral file preview. User submissions and synthetic demonstration records are combined for display but identified separately. Frontend text is escaped. File downloads use attachment disposition; no user path is accepted for storage lookup. Uploads are size-limited and extension-checked, but not malware-scanned. The app is for trusted local use only.

`static/app.js` renders a dark dashboard with exactly nine flat sidebar links matching the reference. The sidebar has no folder tree. A collapsible context selector under the page heading selects Project → Chemistry → Cell Size; module and functional folder dropdowns in the content area preserve the canonical hierarchy. Summary cards and KPI cards open scoped task lists from `/api/cells/<cell_id>/tasks/<group>`. Each task has a stable ID, PIC, due date and status; details include DOE, lot and sample cell identifiers. Data Sources and file paths are not exposed in the UI. All built-in tasks, dates and metric values are synthetic.

KPI edits and custom program labels are stored in browser localStorage only. A custom program refers to an existing canonical cell; it does not add server-side hierarchy or task data. Task templates and summary metrics are demonstration constants, not calculated from uploads or user KPI edits. The UI has no upload action. Existing intake and read-only preview APIs remain available for future integration.

## Production evolution

Move source objects into versioned object storage and metadata to PostgreSQL. Add a source table keyed by digest and document-to-source relationships; replace prototype JSON references with a transactional projection. Enforce source immutability through storage policy and verify checksums at retrieval. Add authenticated team/PIC roles and approval transitions with append-only audit events. A queue should process uploads, scan files, and derive normalized engineering data under versioned processing definitions. Separate observed metrics, units, provenance, test conditions and uncertainty from KPI targets.

Connectors should register original source locations and version identities, not duplicate files across modules. Change watchers can enqueue idempotent processing keyed by source digest; preserve earlier raw versions. Cycler adapters map channels to Cell ID, DOE ID and Build Lot ID, with validation of sample identity and units before publishing calculated metrics. Backend connectors, change watchers and engineering calculations are not implemented in this prototype.

STEP ingestion requires a CAD conversion worker (for example OpenCascade) to create a web-viewable mesh and preserve the original STEP, units and revision association. No 3D viewer is exposed in the redesigned UI. CSV/XLSX/PDF preview is read-only; PDF preview extracts text, not a page rendering.

Publication and restoration must retain the complete `data/` directory. Running Python processes do not survive environment snapshot restoration. No fresh-task restoration has been verified.


## Team entry points and user content contract

`team_folders.py` defines ten short team labels. `storage.initialize()` creates relative symlinks below `data/teams/<Project>/<Chemistry>/<Cell Size>/` pointing to the original module directories below `data/projects/`. No raw data is copied, renamed or deleted. Folder cards are available inside the context panel in the main content area; the sidebar remains flat.

`docs/USER_REQUIREMENTS.tsv` preserves the provided content specification. `configuration/content_catalog.json` maps its 110 source definitions to the canonical modules, with explicit unconnected placeholders for headings whose detailed fields were not provided. `catalog.py` exposes definitions separately from synthetic task results. Source path metadata is kept internally but excluded from the redesigned UI and visible-record CSV export. Formula descriptions are specifications, not executed engineering calculations. Alias paths such as `00_Project_Control`, `05_Testing` and `05_DATA_ANALYTICS` are preserved as provided and do not rename the canonical filesystem modules.
