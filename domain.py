"""Canonical project, chemistry, cell size and module hierarchy."""
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
