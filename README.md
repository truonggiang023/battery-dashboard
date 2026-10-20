# Battery R&D Dashboard

Ứng dụng Python/Flask, giao diện tối theo mẫu, sidebar phẳng và dữ liệu cập nhật từ Excel. **Mỗi mục chức năng là một file `.xlsx`; nội dung con là các sheet**, không tạo file riêng cho từng dòng thông tin.

## Chạy nội bộ

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python serve.py --local --port 5000
```

Dùng Waitress, một process với 8 thread. `--local` chỉ bind loopback và không yêu cầu đăng nhập. Python 3.11+, Linux (`fcntl` để khóa file).

Ứng dụng tự tạo các workbook trống cho 5 cell thật và một **dự án ví dụ riêng**. Khởi động lại không ghi đè file đã tồn tại. Giao diện mặc định mở dự án `[VÍ DỤ] DEMO-LFP-01`; chọn `[THỰC]` để nhập dữ liệu vận hành của cell.

## Cách team cập nhật

1. Chọn **Dự án → Chemistry → Cell Size** bằng đường dẫn dưới tiêu đề.
2. Chọn folder team, hoặc mục ở sidebar.
3. Chọn **File Excel → Sheet → Cập nhật sheet**.
4. Nhập hoặc dán vùng ô từ Excel; cột `*` là bắt buộc. Bấm **Lưu sheet**.
5. File Excel trên server được lưu thật; dashboard tính lại dữ liệu. Tải lại trang vẫn giữ thay đổi.

Có thể chỉnh trực tiếp **file trên server** rồi lưu: dashboard kiểm tra lại mỗi 30 giây. **File tải xuống máy cá nhân là bản sao**; sửa bản sao không tự đồng bộ về server. Không có nút nộp dữ liệu hoặc Data Sources. Không đổi tên sheet/header, không thêm sheet tùy ý và không nhập công thức Excel; nhập giá trị, app tính KPI ở backend.

Bấm **Tải bộ Excel của cell** trong phần chọn cell để lấy toàn bộ file theo team. Xem [hướng dẫn vận hành](docs/OPERATIONS.md), [folder ngắn gọn](docs/TEAM_FOLDERS.md) và [danh mục file/sheet](docs/WORKBOOKS.md).

## File chính

```text
01_PMO/
├── Project Information & KPI.xlsx  # Project Information, Budget
├── Target vs Actual.xlsx          # Targets, Energy density, Cell capacity,
│                                 # Cycle life predicted, Cell cost Prototype/SOP
├── Master Timeline.xlsx           # Project Milestones
├── Cấu trúc & PIC.xlsx
├── Execution Control.xlsx
├── Báo cáo tuần.xlsx
├── Rủi ro & Sự vụ.xlsx
└── Project Status.xlsx
```

Các file còn lại nằm theo team Design, Materials, DOE, Manufacturing, Testing, Analysis, Cost, Data và Documents. Tên sheet có `/` được đổi thành `-` và rút gọn tối đa 31 ký tự theo giới hạn Excel. Header kỹ thuật được ghi trong file mẫu và đánh dấu bắt buộc trong editor. Một số thanh ghi kỹ thuật dùng cột text theo bảng yêu cầu; chúng chưa tự tham gia tính KPI.

## Tổng quan tính từ dữ liệu đã lưu

- Tiến độ: `Σ(weight × completion) / Σ(weight)`, loại milestone Cancelled.
- Ngân sách còn: approved − actual − committed; không tự cộng nhiều currency.
- Milestones: Completed/Approved, có actual date và completion=100.
- Issues: status khác Closed; Critical → Red, overdue/high → Amber, bình thường → Green, chưa có dữ liệu → Grey.
- Energy density: tổng discharge energy / tổng mass của nhóm Approved mới nhất, cùng DOE/condition.
- Capacity: trung bình Approved ở ngày mới nhất, khớp DOE/condition/C-rate/temperature.
- Cycle life: dự đoán Approved, `validated=Yes`, đúng retention threshold; luôn ghi là dự đoán. `validated` và `approval` là xác nhận do team nhập, không phải app tự kiểm định mô hình.
- Cost: quantity × unit price + process + overhead, tách **Prototype** và **SOP**, cùng currency.

Không có số mô phỏng làm fallback trong `[THỰC]`. Dữ liệu thiếu / chưa Approved / điều kiện không thống nhất hiển thị `—` và cảnh báo phù hợp. Task chi tiết lấy từ các sheet, không sinh task giả.

## Cycler = 3D Cell Digital Twin

Đã tích hợp mã từ [truonggiang023/Digital-Twin](https://github.com/truonggiang023/Digital-Twin), commit `1b999d16822729adfb4df463804af0f8906a0034`:

- Tủ Three.js, xoay/zoom/chọn cell, màu theo nhiệt độ.
- Rack gốc 12 kênh; dự án ví dụ prismatic hiển thị 6 kênh được gán dự án đó.
- Start/Pause/Reset/speed dùng cùng mô hình Python gốc. Các lệnh áp dụng toàn rack.
- Chế độ **Trạng thái từ sheet** dùng `Cycler - 3D Cell Digital Twin.xlsx` với `Cell Mapping` / `Cell State`.

**Mô hình gốc 2.5–2.775 Ah, 3.0–4.2 V chưa hiệu chuẩn cho cell LFP 105 Ah.** Mô phỏng chỉ được điều khiển trong dataset ví dụ, không ghi vào KPI Approved và không điều khiển thiết bị thật. Telemetry runtime mất khi Reset/restart; trạng thái đã lưu trong Excel vẫn giữ. Chưa có STEP import hoặc trường nhiệt 3D theo không gian. [Nguồn mã và giới hạn](integrations/digital_twin/PROVENANCE.md).

## Lưu trữ và dùng chung

Dữ liệu thật ở `data/projects/`, ví dụ ở `data/example_data/projects/`. `data/teams/` là shortcut tới module chuẩn. Lần chuyển đổi này chỉ bỏ folder con cũ nếu rỗng; file cũ được giữ nguyên. Các nguồn gốc cũ ở `data/sources/` không bị sửa.

Mỗi lần lưu từ app có bản workbook cũ trong `workbook_history/`, audit, khóa file theo cell và kiểm tra revision chống ghi đè khi hai người cùng sửa. Bản hiện tại được thay bằng thao tác atomic. Sao lưu **toàn bộ `data/`**, gồm history và dữ liệu cũ.

Để dùng chung, đặt `DASHBOARD_USERNAME` và `DASHBOARD_PASSWORD` qua biến môi trường bảo mật của máy chủ rồi chạy:

```bash
.venv/bin/python serve.py --host 0.0.0.0 --port 5000
```

Đặt sau reverse proxy HTTPS và lưu `data/` trên persistent volume. Đây là đăng nhập dùng chung, chưa có tài khoản cá nhân, RBAC hoặc quy trình phê duyệt độc lập. Chưa triển khai host công cộng trong phiên này. Không dùng nhiều WSGI process vì rack mô phỏng là trạng thái chung trong một process. Tránh sửa Excel ngoài server đồng thời với editor; lock của app không được Excel ngoài app tuân theo.

## Kiểm thử

```bash
.venv/bin/python -m unittest discover -s tests -v
node --check static/app.js
```

Bộ kiểm thử xác minh tính KPI, tách dữ liệu thật/ví dụ, revision conflicts, cập nhật Excel ngoài app, điều kiện đo, file history, đăng nhập, mapping cell và safety STOP của mô hình gốc.
