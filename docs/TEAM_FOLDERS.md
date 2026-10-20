# Folder ngắn gọn cho các team

```text
BATTERY_R&D/
├── CYLINDRICAL/
│   ├── LFP/
│   │   ├── 40135/
│   │   └── 21700/
│   └── SIB/
│       ├── 40135/
│       └── 21700/
└── PRISMATIC/
    ├── LFP01/
    │   └── 52148117/
    └── SIB/                 # Chưa có cell size
```

Mỗi **cell** có cùng 10 folder ngắn:

```text
40135/
├── 01_PMO/                  # KPI, task, timeline, báo cáo, issues
├── 02_Design/               # Thông số, điện hóa, cơ khí, bản vẽ
├── 03_Materials/            # Cathode, anode, separator, electrolyte
├── 04_DOE/                  # Kế hoạch, thông số, run, kết quả
├── 05_Manufacturing/        # Electrode, assembly, formation, QC
├── 06_Testing/              # Test plan, matrix, mẫu, kết quả
├── 07_Analysis/             # Electrical, cycling, thermal, failure
├── 08_Cost/                 # Supplier, BOM, quotation, cost
├── 09_Data/                 # Cycler, mapping, processed, simulation
└── 10_Documents/            # Drawings, specifications, standards
```

Folder thực tế nằm tại `data/teams/<Project>/<Chemistry>/<Cell Size>/` (Project giữ tiền tố `01_CYLINDRICAL` hoặc `02_PRISMATIC`). Đây là **shortcut liên kết** tới 10 module chuẩn trong `data/projects/`, không tạo bản sao file. Cấu trúc chi tiết vẫn được giữ nguyên. PRISMATIC/SIB chưa có cell nên chưa tạo folder team.

**Trên dashboard:** bấm đường dẫn cell dưới tiêu đề → chọn Project, Chemistry, Cell Size → chọn folder team. Sidebar chỉ giữ các mục phẳng như ảnh mẫu; không có Data Sources hoặc nút nộp dữ liệu.

Nếu các team đặt file trực tiếp vào folder, file sẽ nằm trong cấu trúc dự án nhưng **chưa tự xuất hiện trên dashboard**; cơ chế đồng bộ/index chưa được tích hợp. Với dữ liệu đã đăng ký, giữ nguyên file gốc trong `data/sources/`; không di chuyển hoặc ghi đè file nguồn. Sao lưu toàn bộ `data/` cùng nhau.
