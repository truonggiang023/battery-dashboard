# Hướng dẫn vận hành theo team

## Bắt đầu

1. Mở dataset `[VÍ DỤ]` để thực hành trên dữ liệu giả lập có nhãn. Bộ này ở thư mục riêng.
2. Chuyển sang dataset `[THỰC]` của đúng form factor, chemistry và cell size.
3. PMO mở **Thông tin dự án**, nhập project_id, project_name, owner, start_date, phase và currency.
4. PMO mở **Master Timeline → Project Milestones**: nhập milestone_id, name, weight, completion (%) và PIC. Actual date là bắt buộc khi Completed/Approved.
5. Nhập ngân sách trong **Project Information & KPI → Budget**. Giữ currency nhất quán. Giá trị chưa có phải để trống; chỉ nhập `0` nếu đã xác nhận bằng 0.
6. Phân công và theo dõi trong **Cấu trúc & PIC**, **Execution Control**, **Rủi ro & Sự vụ**. Task liên kết KPI bằng metric: energy, capacity, cycle, cost_prototype hoặc cost_sop.
7. Team Testing/Data vào **Target vs Actual** để nhập target, kết quả đo, model prediction và cost line phù hợp. Chỉ Approved mới đi lên KPI.

Không sửa bản ví dụ để làm dữ liệu thật: hãy nhập vào `[THỰC]`. Không có cơ chế tự chuyển số liệu ví dụ vào dự án thật.

## Project Information & KPI.xlsx

- **Project Information**: một dòng mỗi cell; project_id, project_name bắt buộc. Cell scope lấy từ folder nên không thể chuyển record qua cell khác bằng cách sửa tên.
- **Budget**: một dòng mỗi hạng mục, item_id duy nhất; approved, actual, committed, forecast cùng currency và có PIC.
- Các KPI tổng hợp về tiến độ, gates và issues được tính từ workbook chuyên trách, không nhập lại để tránh lệch dữ liệu giữa hai file.

## Target vs Actual.xlsx

| Sheet | Nhập gì |
| --- | --- |
| Targets | metric_id, target, unit, condition, DOE; C-rate/temperature cho capacity, EOL retention (%) cho cycle |
| Energy density | discharge_energy_wh, cell_mass_kg, test_date, điều kiện, ID traceability, approval, revision, PIC |
| Cell capacity | value (Ah), c_rate, temperature_c, test_date, điều kiện, ID traceability, approval, revision, PIC |
| Cycle life predicted | forecast_cycles, retention_threshold, model_revision, validated, prediction_date, approval, PIC |
| Cell cost Prototype | Các dòng BOM/process/overhead cho prototype |
| Cell cost SOP | Các dòng riêng cho SOP forecast |

Mỗi ID là duy nhất trong sheet. `cell_id` trong kết quả là ID mẫu thử; model/cell-size scope là folder đang chọn. Không cộng trộn các DOE hoặc điều kiện đo khác nhau. Nếu có nhiều condition/DOE mà Targets chưa chọn cụ thể, KPI giữ trống thay vì tự lấy một kết quả.

Dự đoán cycle chỉ được hiển thị khi có target retention threshold tương ứng, Approved và validated=Yes. App không tự chứng nhận mô hình; team chịu trách nhiệm xác nhận trạng thái này.

## Các team kỹ thuật khác

Chọn folder team → file Excel của mục chức năng → sheet của nội dung con. Các cột được chuẩn hóa từ trường Information trong bảng yêu cầu; thêm entry_id, PIC, revision, approval và các mã traceability. Những thanh ghi này lưu dữ liệu thật nhưng chưa tự chạy tính toán điện hóa hoặc xử lý raw data.

## Cập nhật trực tiếp hoặc qua trình duyệt

- Cập nhật qua **Cập nhật sheet**: hỗ trợ thêm/xóa dòng, dán bảng từ Excel, kiểm tra trường bắt buộc và lưu xuống file server.
- Sửa workbook trực tiếp trên server: giữ nguyên tên và thứ tự header; lưu hoàn chỉnh trước khi dashboard đọc lại. Tự kiểm tra 30 giây; không cần restart.
- Excel tải xuống máy cá nhân là bản sao. Chỉnh bản sao không gửi dữ liệu trở lại server. Không có nút upload.
- Chỉ nhập giá trị, không dùng formula. Mọi tổng hợp KPI được tính ở backend để không phụ thuộc cached formula của Excel.
- Tối đa 5000 dòng mỗi sheet, workbook 10 MB / 50 MB sau giải nén. Raw telemetry lớn cần lưu riêng; sheet dùng cho input/summary/curve đã chọn.

## Hai người cùng sửa

Khi người thứ hai lưu trên revision cũ, app trả lỗi xung đột và giữ dữ liệu đang nhập. Sao chép phần chỉnh sửa cần giữ, bấm **Tải lại file**, nhập lại trên revision mới rồi lưu. Không tự ghi đè dữ liệu mới của đồng nghiệp.

Các file history và audit phục vụ truy vết thay đổi từ app; không có chữ ký phê duyệt hoặc log danh tính cá nhân khi dùng chung tài khoản. Thay đổi Excel ngoài app được phát hiện bằng checksum nhưng không được app chụp history tại đúng thời điểm sửa ngoài; sao lưu hệ thống vẫn cần thiết.

## Cycler / 3D Cell Digital Twin

Bấm **Cycler · 3D Cell Digital Twin** ở vùng nội dung.

- Dataset ví dụ: mô hình gốc từ repo Digital-Twin, Start/Pause/Reset/speed; Reset toàn rack cần xác nhận. Giới hạn mô hình hiển thị ngay trên màn hình.
- **Trạng thái từ sheet**: nhập Cell Mapping trước rồi Cell State. Mapping có Cell ID, model, form_factor, kích thước, revision, device/channel, PIC. State có timestamp ISO-8601 kèm timezone, SOC, V, I, T, cycle, capacity và retention. Dòng State không được trỏ đến Cell ID chưa có; một channel không gán hai cell cùng lúc.
- Hình học theo kích thước trong sheet; chọn cell bằng 3D hoặc dropdown. Slider xem các mốc thời gian đã ghi. Dữ liệu thật chỉ phản ánh trạng thái đã ghi, không giả là kết nối thời gian thực với thiết bị.
- Chưa có adapter tới cycler vật lý, STEP importer, mô hình prismatic riêng hoặc thermal field 3D. Mô hình gốc và NASA ML là minh họa/thử nghiệm, không dùng để điều khiển thiết bị hay xác nhận KPI thực.

## Sao lưu và khôi phục

Dừng app trước khi sao lưu toàn bộ `data/`; giữ project workbooks, example_data, history, audit, sources và metadata cũ. Không chỉ sao lưu code Git. File `.xlsx` cũ trong history có tên SHA-256; trước khi khôi phục hãy sao lưu bản hiện tại và kiểm tra đúng cell/book. Hiện chưa có nút restore để tránh khôi phục nhầm dữ liệu.
