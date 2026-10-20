# Dự án ví dụ cho các team

Tải [EXAMPLE-LFP01-52148117.zip](EXAMPLE-LFP01-52148117.zip).

Ví dụ **PRISMATIC → LFP01 → 52148117**, có file theo từng chức năng và các sheet bên trong. Đây là số liệu minh họa, không phải kết quả thử nghiệm thực tế.

| Nội dung | Giá trị ví dụ | Cách được tính |
| --- | --- | --- |
| Project progress | 68% | Weighted milestones |
| Budget approved | 52 tỷ VND | Tổng các dòng Budget |
| Actual / committed | 31.8 / 4.2 tỷ VND | Tổng theo currency VND |
| Remaining | 16 tỷ VND | 52 − 31.8 − 4.2 |
| Completed gates | 2 / 7 | Approved/Completed, actual date có đủ |
| Open issues | 4 | Chưa Closed, gồm 1 Critical |
| Energy density | 178 Wh/kg | 338.2 Wh / 1.9 kg |
| Cell capacity | 103.2 Ah | Approved, 0.33C / 25°C |
| Predicted cycle life | 2320 cycles | Bản ghi dự đoán mẫu, EOL 80%, model DEMO-A |
| Prototype cost | 22.6 USD/cell | 20 + 2 + 0.6 |
| SOP forecast | 17.8 USD/cell | 16 + 1.5 + 0.3 |

Các file quản lý còn có PIC, tasks, DOE run, weekly report, issue và milestone liên kết bằng ID. Các team kỹ thuật có các dòng cấu trúc mẫu dạng Draft để điền thêm, không có kết quả đo giả được gắn là dữ liệu thực.

App tự tạo cùng bộ ví dụ từ `example_project.py` khi khởi động lần đầu, trong thư mục riêng `data/example_data/`; không ghi vào dataset `[THỰC]`. Không reset file ví dụ sau khi người dùng đã chỉnh sửa.

Cycler 3D dùng lại model của repo Digital-Twin theo phiên bản được ghi trong PROVENANCE. Model gốc khoảng 2.5–2.775 Ah không hiệu chuẩn cho cell 105 Ah ở bảng ví dụ; telemetry mô phỏng không tự ghi vào các sheet Approved.
