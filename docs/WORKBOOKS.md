# Danh mục workbook và sheet

Mỗi mục chức năng = một file Excel. Nội dung con = sheet, không phải folder hoặc file riêng.

| Team/module | File Excel | Sheets |
| --- | --- | --- |
| 00_Project_Management | Project Information & KPI.xlsx | Project Information; Budget |
| 00_Project_Management | Target vs Actual.xlsx | Targets; Energy density; Cell capacity; Cycle life predicted; Cell cost Prototype; Cell cost SOP |
| 00_Project_Management | Master Timeline.xlsx | Project Milestones |
| 00_Project_Management | Rủi ro & Sự vụ.xlsx | Issue Register |
| 00_Project_Management | Execution Control.xlsx | Task Master List; Action Tracking; Deliverables |
| 00_Project_Management | Cấu trúc & PIC.xlsx | Organization Structure; PIC Assignment |
| 00_Project_Management | Báo cáo tuần.xlsx | Weekly Progress; Completed Activities; Next Week Plan; Open Issues |
| 03_DOE | DOE Run Tracking.xlsx | DOE Runs |
| 06_Cell_Analysis | Electrical Performance.xlsx | Performance Curves |
| 08_Data_Analytics | Cycler - 3D Cell Digital Twin.xlsx | Cell Mapping; Cell State |
| 00_Project_Management | Project Status.xlsx | Current Phase - Stage Gate; DOE progress; Milestones tiếp theo; Project warning colors |
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

Các schema chuyên trách quản lý KPI/đo đạc được kiểm tra số, unit, ngày và approval. Các schema kỹ thuật còn lại có cột text từ bảng Information do người dùng cung cấp, không tự chạy mô hình vật lý.

Giữ nguyên tên file, sheet và header; các tên sheet được rút gọn theo giới hạn 31 ký tự của Excel.