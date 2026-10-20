# Danh mục workbook và sheet

30 function theo bảng yêu cầu và 7 workbook hỗ trợ DOE/3D đã có: tổng 37 file cho mỗi cell. Không tạo file riêng cho từng nội dung con. Xem [cây nội dung đầy đủ](CONTENT_TREE.md).

Σ: tổng hợp tự động, chỉ đọc. Các sheet còn lại là dữ liệu đầu vào.

| Team/module | File Excel | Sheets |
| --- | --- | --- |
| 00_Project_Management | Project Information & KPI.xlsx | Project Information; Σ Tiến độ dự án (%); Budget; Σ Milestones hoàn thành; Σ Issues đang mở |
| 00_Project_Management | Target vs Actual.xlsx | Energy density; Cell capacity; Cycle life predicted; Σ Cell cost - Prototype - SOP; Targets; Cell cost Prototype; Cell cost SOP |
| 00_Project_Management | Master Timeline.xlsx | Project Milestones; Σ Gantt Chart; Σ Planned vs Actual; Σ Critical Activities |
| 00_Project_Management | Rủi ro & Sự vụ.xlsx | Issue Register |
| 00_Project_Management | Execution Control.xlsx | Task Master List; Action Tracking; Deliverables; Σ Pending - Overdue |
| 00_Project_Management | Cấu trúc & PIC.xlsx | Organization Structure; PIC Assignment |
| 00_Project_Management | Báo cáo tuần.xlsx | Weekly Progress; Completed Activities; Next Week Plan; Open Issues |
| 03_DOE | DOE Run Tracking.xlsx | DOE Runs |
| 06_Cell_Analysis | Electrical Performance.xlsx | Σ Capacity Test; Σ Energy - Efficiency; DCIR - Impedance; Σ Voltage Curves; Σ Energy Density; Performance Curves; Efficiency Inputs |
| 08_Data_Analytics | Cycler - 3D Cell Digital Twin.xlsx | Cell Mapping; Cell State |
| 00_Project_Management | Project Status.xlsx | Σ Current Phase - Stage Gate; Σ DOE progress; Σ Milestones tiếp theo; Σ Project warning colors |
| 01_Cell_Design | Cell Specifications.xlsx | Cell identity; Electrical targets; Energy & power; Physical envelope; Reliability & safety; Cost & compliance |
| 01_Cell_Design | DOE Master Plan.xlsx | Cell balancing; Electrode dimensions; Cathode design; Anode design; Electrolyte design; Design calculations |
| 01_Cell_Design | Mechanical Design.xlsx | 2D - 3D Drawings; Specifications - GD&T |
| 02_Materials | Cathode.xlsx | Active material - Grade; Conductive additive; Binder 1 - Binder 2; Dispersant - Solvent; Aluminum foil; Coating composition - specifica |
| 02_Materials | Anode.xlsx | Active material - Grade; Conductive additive; Binder 1 - Binder 2; Dispersant - Solvent; Cu - Al foil; Coating composition - specifica |
| 02_Materials | Other Materials.xlsx | Separator; Electrolyte |
| 03_DOE | DOE Master Plan.xlsx | DOE Master Plan |
| 03_DOE | DOE Design Parameters.xlsx | DOE Design Parameters |
| 03_DOE | DOE Results.xlsx | DOE Results |
| 03_DOE | DOE Comparison.xlsx | DOE Comparison |
| 04_Cell_Manufacturing | Electrode Manufacturing.xlsx | Mixing; Coating; Drying - Calendering; Slitting - Notching; Electrode QC |
| 04_Cell_Manufacturing | Cell Assembly.xlsx | Notching; Winding - Stacking; Tab welding - CC welding; Can-Cap - Sealing assembly; Electrolyte filling; Final sealing - Leak check |
| 04_Cell_Manufacturing | Formation & Aging.xlsx | Formation recipe; Formation curves; RT - HT Aging; Grading - OCV - DCIR; Formation yield |
| 04_Cell_Manufacturing | Production Control.xlsx | Build Tracking; Process Parameter History; Process QC - Defect; Yield and Scrap; Traceability |
| 05_Validation_Testing | Test Categories.xlsx | Electrical Tests; Mechanical Tests; Safety Tests; Environmental Tests; Test Data - Reports |
| 06_Cell_Analysis | Cycle Life Analysis.xlsx | Capacity Retention; Coulombic Efficiency; Cycle Life Prediction; Degradation - dQdV |
| 06_Cell_Analysis | Thermal - Mechanical - Failure.xlsx | Thermal rise - Hotspots; Thermal simulation; Compression - Vibration - Drop; Vent - Burst - Leak; Teardown visual - SEM - EDS; Failure Mode - RCA - CAPA |
| 07_Supplier_Cost | Supplier Management.xlsx | Supplier Management |
| 07_Supplier_Cost | BOM & Cost.xlsx | BOM & Cost |
| 08_Data_Analytics | Cycler Data.xlsx | Cycler Raw Data; Processed Curve Data; Cycler Channel - Cell Mapping; Cell Performance Summary; Data Quality - Sync Status |
| 08_Data_Analytics | Engineering Data & Dashboard.xlsx | Simulation Data; DOE Comparison Analytics |
| 08_Data_Analytics | 3D Virtual Operation.xlsx | 3D Virtual Operation |
| 09_Document_Control | Engineering Documents.xlsx | Engineering Drawings; Technical Specifications; Standards - Requirements |
| 05_Validation_Testing | Test Plan.xlsx | Test Plan |
| 05_Validation_Testing | Test Matrix.xlsx | Test Matrix |
| 05_Validation_Testing | Sample Tracking.xlsx | Sample Tracking |

Giữ nguyên header và tên sheet. Excel giới hạn tên sheet 31 ký tự; giao diện vẫn hiện đầy đủ tên nội dung gốc. Không nhập công thức Excel hoặc tự thêm tab; nhập giá trị ở tab nguồn. Sheet tổng hợp được app tính lại khi đọc/cập nhật/xuất file.
