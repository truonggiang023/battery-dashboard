# VoltLab · Battery R&D Dashboard

Python / Flask interactive prototype for battery cell development, with a canonical project tree, Plotly charts and local team file intake.

## Run

```bash
cd /workspace/battery-dashboard
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

The development server listens on port 5000. No external database or credentials are required. Plotly is vendored locally with its license; fonts have system fallbacks.

## Cây thư mục cho các team

Chọn **Project → Chemistry → Cell Size** rồi mở module và thư mục chức năng để tra cứu dữ liệu. Giao diện không có nút hoặc form nộp dữ liệu.

Xem [cây folder đầy đủ](docs/FOLDER_TREE.md). Hệ thống tự tạo thư mục trong `data/projects/` cho 5 cell, gồm 10 module chuẩn mỗi cell. PRISMATIC / SIB được giữ nguyên, chưa cấu hình cell size.

File nguồn và metadata đã có được giữ nguyên. Backend intake vẫn tồn tại để tích hợp sau này; thao tác chép file trực tiếp vào folder chưa tự tạo record trên dashboard. Sao lưu toàn bộ `data/` cùng nhau.

## Verified capabilities

- Expandable project / chemistry / cell / module / folder tree, search, collapse and breadcrumbs.
- Isolated records by cell, status and text filters, source metadata, CSV export.
- Sample cycle life, discharge and DOE charts with Plotly; synthetic interactive 3D cylinder.
- In-memory read-only CSV, XLSX and PDF-text preview, limited to 20 rows / 2 pages.
- Local file intake with SHA-256 deduplication and revision conflict protection.

**All KPI cards, charts, milestones and built-in records are synthetic, fixed demonstration examples.** Uploaded records are labeled separately and are not automatically interpreted as validated engineering results. STEP files can be stored/downloaded; CATIA STEP parsing/viewing is not implemented. The 3D demo is generated geometry, not a CAD conversion.

## Validation

```bash
.venv/bin/python -m unittest discover -s tests -v
node --check static/app.js
```

## Before shared production use

This is a local prototype with no authentication or authorization; anyone with server access can upload/download. It has no approval transition workflow, source watchers, external connectors or automatic KPI calculations. Do not expose publicly or upload sensitive engineering data until these are implemented. Use production WSGI hosting, identity/roles, malware scanning, audit logs, backups and object storage before team deployment.

See [architecture](docs/ARCHITECTURE.md) for extension points.
