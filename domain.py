"""Canonical hierarchy and synthetic demo records. No real engineering results."""
MODULES = [
('00_Project_Management', ['Project Information & KPI','Target vs Actual','Project Status','Organization Structure & PIC','Execution Control','Master Timeline','Weekly Report','Risk & Issue Register']),
('01_Cell_Design',['Cell Specifications','Electrochemical Design','Mechanical Design','2D & 3D Drawings','Specifications & GD&T','Design Revision']),
('02_Materials',['Cathode','Anode','Separator','Electrolyte','Other Materials','Material BOM & COA']),
('03_DOE',['DOE Master Plan','DOE Design Parameters','DOE Run Tracking','DOE Results','DOE Comparison']),
('04_Cell_Manufacturing',['Electrode Manufacturing','Cell Assembly','Formation & Aging','Production Control','Process QC & Yield','Cell Traceability']),
('05_Validation_Testing',['Test Plan & Matrix','Sample Tracking','Electrical Tests','Mechanical Tests','Safety Tests','Environmental Tests','Test Data & Reports']),
('06_Cell_Analysis',['Electrical Performance','Cycle Life Analysis','Thermal Analysis','Mechanical Analysis','Teardown / SEM / EDS','Failure Analysis / RCA / CAPA']),
('07_Supplier_Cost',['Supplier Management','Supplier Quotation','Cell BOM','Prototype & SOP Cost','Cost Tracking']),
('08_Data_Analytics',['Cycler Raw Data','Processed Curve Data','Cycler Channel / Cell Mapping','Cell Performance Summary','Simulation Data','DOE Comparison Analytics','3D Virtual Operation','Dashboard Reports']),
('09_Document_Control',['Engineering Drawings','Technical Specifications','Standards & Requirements','Revision History','Approved Documents'])]
PROJECTS = [dict(id='CYL', name='01_CYLINDRICAL', chemistries=[dict(id='CYL-LFP',name='LFP',sizes=['40135','21700']),dict(id='CYL-SIB',name='SIB',sizes=['40135','21700'])]),dict(id='PRI',name='02_PRISMATIC',chemistries=[dict(id='PRI-LFP01',name='LFP01',sizes=['52148117']),dict(id='PRI-SIB',name='SIB',sizes=[])])]
CELLS = {f"{c['id']}-{s}":dict(id=f"{c['id']}-{s}",size=s,chemistry=c['name'],project=p['name']) for p in PROJECTS for c in p['chemistries'] for s in c['sizes']}
OWNERS = ['Project office','Cell design','Materials team','DOE team','Process engineering','Validation team','Cell analysis','Purchasing','Data engineering','Document control']

def records(cell_id, module):
    """Sources are referenced once by stable ID; row links carry provenance separately."""
    name, folders = MODULES[module]
    return [dict(id=f'{cell_id}-{module:02}-{i:02}',content=folder,information=[f'{cell_id} · baseline review', 'Revision B · engineering review', 'Sample dataset · 24 records'][i%3],source_id=f'{cell_id}-SRC-{module:02}-{i:02}',source_path=f'demo://{cell_id}/{name}/{i+1:02}.csv',pic=OWNERS[module],status=['Approved','In review','Planned'][i%3],revision='B' if i%3==1 else 'A',approval='Approved' if i%3==0 else 'Draft',doe_id=f'{cell_id}-DOE-002',build_lot_id=f'{cell_id}-LOT-024',cell_id=f'{cell_id}-CELL-001') for i,folder in enumerate(folders)]

TASK_GROUPS = {
    'progress': ('Tiến độ dự án', '68%', 'DOE vòng 2 · 8/12 hoạt động đã hoàn thành', 0),
    'budget': ('Ngân sách', '52 tỷ VND', 'Đã chi 31.8 tỷ · Theo dõi chi phí dự án', 7),
    'milestones': ('Milestones', '2/7', 'Hai gate đã hoàn thành trong bộ dữ liệu mô phỏng', 0),
    'issues': ('Issues đang mở', '4', '1 critical · 3 medium · Dữ liệu mô phỏng', 0),
    'energy': ('Energy density', '178 Wh/kg', 'Target: 185 Wh/kg · Chưa đạt', 1),
    'capacity': ('Cell capacity', '103.2 Ah', 'Target: 105 Ah · Chưa đạt', 5),
    'cycle': ('Cycle life (dự đoán)', '2320 cycles', 'Target: 2500 cycles · Dự đoán minh họa', 6),
    'cost': ('Cell cost', '22.6 USD/cell', 'Target: 21.8 USD/cell · Chưa đạt', 7),
}
# title, PIC, due date, status, detailed action; all entries below are synthetic.
TASK_TEMPLATES = {
 'progress': [('Chốt kế hoạch DOE vòng 2','DOE team','2026-10-25','Đang làm','Review thông số DOE, số lượng mẫu và lịch build.'),('Xác nhận vật liệu cho DOE vòng 2','Materials team','2026-10-18','Quá hạn','Xác nhận COA và lịch giao cathode trước khi build.'),('Review baseline thiết kế','Cell design','2026-10-12','Hoàn thành','Baseline được review trong kịch bản mô phỏng.')],
 'budget': [('Review chi phí prototype','Purchasing','2026-10-28','Đang làm','Đối chiếu quotation, chi phí BOM và chi phí gia công.'),('Xác nhận quotation prototype','Purchasing','2026-11-02','Chưa bắt đầu','Tổng hợp báo giá nhà cung cấp và trình duyệt dự toán.'),('Đối chiếu ngân sách đã chi','Project office','2026-10-20','Đang làm','Đối chiếu các hạng mục chi phí với ngân sách kế hoạch.')],
 'milestones': [('Concept review','Project office','2026-09-15','Hoàn thành','Actual: 15/09/2026 · Demo gate 1 đã hoàn tất.'),('Baseline design review','Cell design','2026-10-01','Hoàn thành','Actual: 01/10/2026 · Demo gate 2 đã hoàn tất.'),('DOE Round 2','Process engineering','2026-11-10','Đang làm','Forecast trễ 31 ngày so với baseline minh họa.'),('A-Sample','Validation team','2026-12-20','Chưa bắt đầu','Forecast trễ 5 ngày; phụ thuộc DOE Round 2.'),('Design Freeze','Cell design','2027-01-15','Chưa bắt đầu','Xác nhận thiết kế và bộ thông số trước khi freeze.'),('B-Sample','Process engineering','2027-02-20','Chưa bắt đầu','Build mẫu sau khi design freeze.'),('SOP readiness','Project office','2027-04-01','Chưa bắt đầu','Review tổng thể quy trình, chất lượng và validation.')],
 'issues': [('Xác nhận vật liệu cho DOE vòng 2','Materials team','2026-10-18','Quá hạn','Critical · Thiếu xác nhận COA; ảnh hưởng lịch build.'),('Review cell capacity dưới target','Cell design','2026-10-25','Đang làm','Medium · Liên kết KPI Cell capacity, target minh họa 105 Ah.'),('Hoàn tất test matrix A-Sample','Validation team','2026-10-30','Đang làm','Medium · Hoàn tất test matrix và phân bổ mẫu thử.'),('Xác nhận quotation prototype','Purchasing','2026-11-02','Chưa bắt đầu','Medium · Chờ báo giá trước khi chốt chi phí prototype.')],
 'energy': [('Review mass breakdown','Cell design','2026-10-24','Đang làm','Đối chiếu khối lượng cell và BOM để xác định nguồn chênh lệch Wh/kg.'),('Phân tích loading cathode','Materials team','2026-10-27','Chưa bắt đầu','So sánh loading và porosity giữa các DOE; không thay đổi raw data.'),('Xác nhận phép tính energy density','Cell analysis','2026-10-29','Chưa bắt đầu','Review tích phân discharge energy và khối lượng tương ứng.')],
 'capacity': [('Review cell capacity dưới target','Cell design','2026-10-25','Đang làm','Kiểm tra điều kiện đo, lượng vật liệu hoạt tính và phân bố dung lượng.'),('Kiểm tra mapping cycler / Cell ID','Data engineering','2026-10-24','Đang làm','Xác nhận mapping channel, sample cell và build lot.'),('Chạy xác nhận dung lượng A-Sample','Validation team','2026-10-30','Chưa bắt đầu','Xác nhận protocol charge/discharge và điều kiện nhiệt độ.')],
 'cycle': [('Review mô hình dự đoán cycle life','Cell analysis','2026-10-28','Đang làm','Phân biệt dữ liệu đo với extrapolation và ghi rõ giới hạn mô hình.'),('Đánh giá fade theo DOE','DOE team','2026-10-30','Chưa bắt đầu','So sánh retention tại cùng điều kiện và mốc cycle.'),('Review protocol aging','Validation team','2026-11-04','Chưa bắt đầu','Kiểm tra SOC window, C-rate và nhiệt độ thử nghiệm.')],
 'cost': [('Tối ưu cell BOM','Purchasing','2026-10-28','Đang làm','So sánh chi phí vật liệu và target minh họa 21.8 USD/cell.'),('Xác nhận quotation prototype','Purchasing','2026-11-02','Chưa bắt đầu','Tổng hợp báo giá và điều kiện thương mại.'),('Review yield và scrap cost','Process engineering','2026-11-05','Chưa bắt đầu','Xác nhận yield theo process; phân tách prototype và SOP cost.')]
}

def tasks(cell_id, group):
    return [dict(id=f'{cell_id}-{group}-TASK-{i+1:03}', content=t[0],information=t[4],pic=t[1],due=t[2],status=t[3],source_id=f'{cell_id}-TASK-SRC-{group}-{i+1:03}',source_path=f'demo://{cell_id}/tasks/{group}/{i+1:03}.csv',doe_id=f'{cell_id}-DOE-002',build_lot_id=f'{cell_id}-LOT-024',cell_id=f'{cell_id}-CELL-001',demo=True) for i,t in enumerate(TASK_TEMPLATES[group])]
