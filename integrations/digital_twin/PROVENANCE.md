# Digital Twin integration

Source requested by the user: https://github.com/truonggiang023/Digital-Twin

Pinned upstream commit: `1b999d16822729adfb4df463804af0f8906a0034`.

- `model.py` is upstream `main.py`, with its `aging` import made relative.
- `rack.py` is the upstream `Rack` class from `server.py`, with relative imports.
- `aging.py`, `live_features.py`, `ml_inference.py` and `models/nasa-forest.json` are copied from that revision.
- `static/vendor/three/` contains upstream bundled Three.js 0.180.0 and its MIT license.
- `static/twin_viewer.js` adapts the original 12-channel rack geometry and selection/color behavior to this dashboard. Backend control and authentication are provided by this app, not the upstream HTTP server.

The simulator is the prior project's generic 2.5–2.775 Ah, 3.0–4.2 V model. It is not a calibrated 105 Ah LFP cell model. Original 12 channel identities, 6 prismatic / 6 cylindrical allocation, rack-wide controls and latched simulated safety stop are retained. Experimental NASA ML is not used as an Approved workbook KPI. Simulated telemetry is kept separate from workbook-entered measured results and never updates live project workbooks automatically.

No hardware control, native STEP import, external BatteryTwin API or calibrated spatial thermal field is included.
