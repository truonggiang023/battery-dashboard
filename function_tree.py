"""The user's 30 functions and 110 content items, verbatim display labels.

Project/chemistry/cell selection stays outside this content hierarchy.
"""
GROUPS = [
 (0,'QUẢN LÝ DỰ ÁN',[
  ('Project Information & KPI',['Project Information','Tiến độ dự án (%)','Ngân sách','Milestones hoàn thành','Issues đang mở']),
  ('Target vs Actual',['Energy density (Wh/kg)','Cell capacity (Ah)','Cycle life predicted','Cell cost — Prototype / SOP']),
  ('Project Status',['Current Phase / Stage Gate','DOE progress','Milestones tiếp theo','Project warning colors']),
  ('Cấu trúc & PIC',['Organization Structure','PIC Assignment']),
  ('Execution Control',['Task Master List','Action Tracking','Deliverables','Pending / Overdue']),
  ('Master Timeline',['Project Milestones','Gantt Chart','Planned vs Actual','Critical Activities']),
  ('Báo cáo tuần',['Weekly Progress','Completed Activities','Next Week Plan','Open Issues']),
  ('Rủi ro & Sự vụ',['Issue Register'])]),
 (1,'Thiết kế Cell',[
  ('Cell Specifications',['Cell identity','Electrical targets','Energy & power','Physical envelope','Reliability & safety','Cost & compliance']),
  ('DOE Master Plan',['Cell balancing','Electrode dimensions','Cathode design','Anode design','Electrolyte design','Design calculations']),
  ('Mechanical Design',['2D / 3D Drawings','Specifications / GD&T'])]),
 (2,'Nguyên vật liệu',[
  ('Cathode',['Active material / Grade','Conductive additive','Binder 1 / Binder 2','Dispersant / Solvent','Aluminum foil','Coating composition / specification']),
  ('Anode',['Active material / Grade','Conductive additive','Binder 1 / Binder 2','Dispersant / Solvent','Cu / Al foil','Coating composition / specification']),
  ('Other Materials',['Separator','Electrolyte'])]),
 (4,'Sản xuất Cell',[
  ('Electrode Manufacturing',['Mixing','Coating','Drying / Calendering','Slitting / Notching','Electrode QC']),
  ('Cell Assembly',['Notching','Winding / Stacking','Tab welding / CC welding','Can-Cap / Sealing assembly','Electrolyte filling','Final sealing / Leak check']),
  ('Formation & Aging',['Formation recipe','Formation curves','RT / HT Aging','Grading / OCV / DCIR','Formation yield']),
  ('Production Control',['Build Tracking','Process Parameter History','Process QC / Defect','Yield and Scrap','Traceability'])]),
 (6,'Phân tích Cell',[
  ('Electrical Performance',['Capacity Test','Energy / Efficiency','DCIR / Impedance','Voltage Curves','Energy Density']),
  ('Cycle Life Analysis',['Capacity Retention','Coulombic Efficiency','Cycle Life Prediction','Degradation / dQdV']),
  ('Thermal / Mechanical / Failure',['Thermal rise / Hotspots','Thermal simulation','Compression / Vibration / Drop','Vent / Burst / Leak','Teardown visual / SEM / EDS','Failure Mode / RCA / CAPA'])]),
 (5,'VALIDATION & TESTING',[
  ('Test Plan',['Test Plan']),('Test Matrix',['Test Matrix']),('Sample Tracking',['Sample Tracking']),
  ('Test Categories',['Electrical Tests','Mechanical Tests','Safety Tests','Environmental Tests','Test Data / Reports'])]),
 (7,'SUPPLIER & COST',[('Supplier Management',[]),('BOM & Cost',[])]),
 (8,'DATA & ANALYTICS',[
  ('Cycler Data',['Cycler Raw Data','Processed Curve Data','Cycler Channel / Cell Mapping','Cell Performance Summary','Data Quality / Sync Status']),
  ('Engineering Data & Dashboard',['Simulation Data','DOE Comparison Analytics'])]),
 (9,'DOCUMENT CONTROL',[
  ('Engineering Documents',['Engineering Drawings','Technical Specifications','Standards / Requirements'])]),
]
