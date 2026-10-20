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
