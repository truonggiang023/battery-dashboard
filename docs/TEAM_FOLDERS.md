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

**Trên dashboard:** bấm đường dẫn cell dưới tiêu đề → chọn Project, Chemistry, Cell Size → chọn folder team → chọn **file Excel và sheet**. Sidebar giữ các mục phẳng như ảnh; không có Data Sources hoặc nút nộp dữ liệu.

**Mỗi mục chức năng là một file Excel, nội dung con là sheet.** Ví dụ PMO có `Project Information & KPI.xlsx`, `Target vs Actual.xlsx`, `Master Timeline.xlsx`. Không tạo file riêng cho từng KPI hoặc mỗi dòng thông tin. Xem [danh mục file/sheet](WORKBOOKS.md).

Cập nhật bằng **Cập nhật sheet** trong app hoặc chỉnh trực tiếp workbook trên server đúng schema. Các file Excel quản lý được đọc lại sau mỗi lần lưu và kiểm tra định kỳ 30 giây. File Excel tải về máy cá nhân là bản sao, không tự đồng bộ; file tùy ý chép vào folder không tự trở thành dữ liệu dashboard.

Dữ liệu ví dụ ở `data/example_data/`, tách biệt với dữ liệu thật. Raw data cũ vẫn được giữ nguyên ở `data/sources/`. Sao lưu toàn bộ `data/` cùng workbook history.
