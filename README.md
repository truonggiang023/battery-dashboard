# Battery R&D Dashboard · Python

Dashboard Flask với giao diện nền tối theo mẫu: sidebar phẳng, tổng quan dự án và liên kết task chi tiết.

## Chạy ứng dụng

```bash
cd /workspace/battery-dashboard
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Server phát triển dùng port 5000. Plotly được lưu local kèm license. Không cần tài khoản hoặc database ngoài.

## Folder ngắn gọn cho các team

Xem [cấu trúc team](docs/TEAM_FOLDERS.md). Các folder `01_PMO` đến `10_Documents` nằm dưới `data/teams/<Project>/<Chemistry>/<Cell Size>/`, liên kết tới 10 module chuẩn, không sao chép dữ liệu. Bấm đường dẫn cell dưới tiêu đề để mở bộ chọn và folder của team.

## Điều hướng

Sidebar chỉ có các mục giống ảnh mẫu:

- **QUẢN LÝ DỰ ÁN:** Tổng quan dự án, Cấu trúc & PIC, Execution Control, Master Timeline, Báo cáo tuần, Rủi ro & sự vụ.
- **PHÁT TRIỂN CELL:** DOE & Thử nghiệm, Công thức DOE, BOM & Vật liệu.

Không có cây thư mục trên sidebar. Bấm đường dẫn cell dưới tiêu đề để mở bộ chọn **Project → Chemistry → Cell Size**. Các module và thư mục chức năng chi tiết nằm trong dropdown ở trang nội dung; cấu trúc chuẩn vẫn được giữ nguyên.

## Tổng quan → Task chi tiết

- Bấm thẻ **Tiến độ, Ngân sách, Milestones hoặc Issues** để mở danh sách task liên quan.
- Bấm từng KPI **Energy density, Cell capacity, Cycle life hoặc Cell cost** để xem task của KPI đó.
- Bấm **Chi tiết** trong bảng để xem task ID, PIC, deadline, trạng thái, DOE ID, Build Lot ID và Cell ID.
- Mỗi cell có phạm vi task riêng; tìm kiếm, lọc trạng thái và xuất CSV từ danh sách.
- Bấm **Tổng quan dự án** ở sidebar để quay lại.

**Cập nhật KPI** và **Dự án mới** là thao tác mô phỏng, chỉ lưu tại trình duyệt theo cell. Dự án mới tạo nhãn chương trình gắn với cell hiện có, không tạo project/chemistry/cell mới trên backend. Các task và thông số ngân sách/tiến độ mẫu không tự tính lại từ KPI đã sửa.

## Nội dung theo yêu cầu

Bảng nội dung được cấu hình từ file người dùng cung cấp trong `configuration/content_catalog.json`; bản gốc nằm tại `docs/USER_REQUIREMENTS.tsv`. Đường dẫn và công thức được giữ nội bộ để tích hợp sau này. UI không hiển thị Data Sources, không có cây folder trong sidebar và không có nút nộp dữ liệu. Các định nghĩa chưa có dữ liệu thật hiển thị trạng thái xám **Chưa kết nối**.

## Dữ liệu và giới hạn

**Tất cả số liệu tổng quan, task, biểu đồ, deadlines và nguồn `demo://` là dữ liệu minh họa, không phải kết quả thử nghiệm thực tế.** Biểu đồ có chế độ DOE theo tuần, cycle life và discharge.

[Cây folder đầy đủ](docs/FOLDER_TREE.md) vẫn được tạo trong `data/projects/` cho 5 cell, mỗi cell có 10 module. PRISMATIC / SIB chưa có cell size. Ký tự `/` trong tên thư mục được đổi thành ` - ` trên filesystem.

File đã có và metadata được giữ nguyên: `data/sources/` chứa nguồn SHA-256, `data/metadata.sqlite3` chứa metadata, folder chứa liên kết `.source.json`. Sao lưu toàn bộ `data/` cùng nhau. Chép file trực tiếp vào folder chưa tự tạo record trên dashboard. Giao diện không có nút hoặc form nộp dữ liệu.

Backend intake và preview vẫn tồn tại để tích hợp sau này. Prototype chưa có đăng nhập, phân quyền, quy trình duyệt, đồng bộ nguồn hoặc tính KPI tự động. STEP có thể lưu/tải qua API nhưng chưa có bộ đọc/viewer STEP. Preview backend hỗ trợ CSV, XLSX và trích xuất text PDF. Không expose công khai hoặc đưa dữ liệu kỹ thuật nhạy cảm lên prototype.

## Kiểm tra

```bash
.venv/bin/python -m unittest discover -s tests -v
node --check static/app.js
```

Xem [kiến trúc](docs/ARCHITECTURE.md) cho các hướng tích hợp dữ liệu thật.
