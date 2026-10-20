# Cây folder đang vận hành

Project → Chemistry → Cell Size → Team/module → File chức năng → Sheet.

```text
BATTERY R&D
01_CYLINDRICAL
  LFP
    40135
    21700
  SIB
    40135
    21700
02_PRISMATIC
  LFP01
    52148117
  SIB
    [Chưa cấu hình Cell Size]
```

Mỗi cell có cùng 10 module. Tên ngắn ở `data/teams/` là shortcut; file thật nằm ở `data/projects/`.

```text
40135/
  00_Project_Management/
    Project Information & KPI.xlsx
    Target vs Actual.xlsx
    Master Timeline.xlsx
    Rủi ro & Sự vụ.xlsx
    Execution Control.xlsx
    Cấu trúc & PIC.xlsx
    Báo cáo tuần.xlsx
    Project Status.xlsx
  01_Cell_Design/
    Cell Specifications.xlsx
    DOE Master Plan.xlsx
    Mechanical Design.xlsx
  02_Materials/
    Cathode.xlsx
    Anode.xlsx
    Other Materials.xlsx
  03_DOE/
    DOE Run Tracking.xlsx
    DOE Master Plan.xlsx
    DOE Design Parameters.xlsx
    DOE Results.xlsx
    DOE Comparison.xlsx
  04_Cell_Manufacturing/
    Electrode Manufacturing.xlsx
    Cell Assembly.xlsx
    Formation & Aging.xlsx
    Production Control.xlsx
  05_Validation_Testing/
    Test Categories.xlsx
    Test Plan.xlsx
    Test Matrix.xlsx
    Sample Tracking.xlsx
  06_Cell_Analysis/
    Electrical Performance.xlsx
    Cycle Life Analysis.xlsx
    Thermal - Mechanical - Failure.xlsx
  07_Supplier_Cost/
    Supplier Management.xlsx
    BOM & Cost.xlsx
  08_Data_Analytics/
    Cycler - 3D Cell Digital Twin.xlsx
    Cycler Data.xlsx
    Engineering Data & Dashboard.xlsx
    3D Virtual Operation.xlsx
  09_Document_Control/
    Engineering Documents.xlsx
```

Nội dung chi tiết nằm trong sheet, không tạo thêm thư mục con rỗng. Những folder cũ có dữ liệu được giữ nguyên. Xem [danh mục sheet](WORKBOOKS.md).