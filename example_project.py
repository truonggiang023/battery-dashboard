"""Explicit example inputs, stored outside live workbooks. Never seed live data."""
from datetime import datetime, timedelta
from pathlib import Path
import math
import workbook_store as store

EXAMPLE_CELL='PRI-LFP01-52148117'

def inputs():
    milestones=[]
    for ident,name,weight,completion,baseline,forecast,actual,status in [
      ('M01','Concept Review',15,100,'2026-09-15','2026-09-15','2026-09-15','Approved'),
      ('M02','Baseline Design',15,100,'2026-10-01','2026-10-01','2026-10-01','Approved'),
      ('M03','DOE Round 2',20,90,'2026-10-10','2026-11-10',None,'In progress'),
      ('M04','A-Sample',15,60,'2026-12-15','2026-12-20',None,'In progress'),
      ('M05','Design Freeze',15,50,'2027-01-15','2027-01-15',None,'In progress'),
      ('M06','B-Sample',10,20,'2027-02-20','2027-02-20',None,'In progress'),
      ('M07','SOP Readiness',10,15,'2027-04-01','2027-04-01',None,'In progress')]:
        milestones.append(dict(milestone_id=ident,name=name,weight=weight,completion=completion,baseline=baseline,forecast=forecast,actual=actual,status=status,pic='PMO · Demo',depends_on=f'M{int(ident[1:])-1:02}' if ident!='M01' else None))
    result={
      'project':{'Project Information':[dict(project_id='DEMO-LFP-01',project_name='LFP Fast Charge EV 105Ah · VÍ DỤ',cell_type='Prismatic LFP01 52148117',start_date='2026-09-01',phase='DOE vòng 2',owner='PMO · Demo',currency='VND')],
        'Budget':[dict(item_id='B01',description='Materials · ví dụ',approved=20_000_000_000,actual=13_800_000_000,committed=2_000_000_000,forecast=19_000_000_000,currency='VND',pic='Purchasing · Demo'),dict(item_id='B02',description='Prototype builds · ví dụ',approved=20_000_000_000,actual=12_000_000_000,committed=1_500_000_000,forecast=19_500_000_000,currency='VND',pic='Manufacturing · Demo'),dict(item_id='B03',description='Validation · ví dụ',approved=12_000_000_000,actual=6_000_000_000,committed=700_000_000,forecast=11_000_000_000,currency='VND',pic='Testing · Demo')]},
      'timeline':{'Project Milestones':milestones},
      'issues':{'Issue Register':[
        dict(issue_id='I01',title='Xác nhận COA cho cathode lot DEMO',severity='Critical',status='Open',due_date='2026-10-18',pic='Materials · Demo',action='Hoàn tất review COA trước build DOE.',evidence='DEMO-COA-001'),
        dict(issue_id='I02',title='Capacity dưới target',severity='Medium',status='In progress',due_date='2026-10-25',pic='Cell Design · Demo',action='Review sample mapping và protocol 0.33C, 25°C.',evidence='DEMO-CAP-001'),
        dict(issue_id='I03',title='Hoàn tất test matrix A-Sample',severity='High',status='In progress',due_date='2026-10-30',pic='Validation · Demo',action='Phân bổ sample theo test category.',evidence=None),
        dict(issue_id='I04',title='Xác nhận quotation prototype',severity='Medium',status='Open',due_date='2026-11-02',pic='Purchasing · Demo',action='Review báo giá theo BOM revision A.',evidence=None)]},
      'pic':{'Organization Structure':[dict(role_id='R01',department='R&D',role='Project Manager',pic='PMO · Demo',reporting_to='R&D Director · Demo')],
        'PIC Assignment':[dict(activity_id='T01',department='Cell Design',role='Design Engineer',pic='Cell Design · Demo',backup='Testing · Demo',deadline='2026-10-25',reporting_to='PMO · Demo')]},
      'weekly':{'Weekly Progress':[dict(record_id='W01',reporting_week='2026-10-19',task_id='T01',status='In progress',evidence='DEMO-REVIEW-001',next_week_plan='Chốt protocol xác nhận dung lượng.',pic='Cell Design · Demo')]},
      'doe_runs':{'DOE Runs':[dict(doe_id=f'DOE-{i:03}',name=f'DOE run {i:02} · ví dụ',status='Approved' if i<=8 else 'In progress' if i<=12 else 'Planned',pic='DOE team · Demo',planned_date='2026-10-15',completed_date='2026-10-18' if i<=8 else None,build_lot_id=f'LOT-DEMO-{i:03}') for i in range(1,19)]},
      'targets':{
        'Targets':[dict(metric_id=m,target=t,unit=u,condition='0.33C / 25C' if m in ('energy','capacity','cycle') else None,doe_id='DOE-002' if m in ('energy','capacity','cycle') else None,c_rate=.33 if m=='capacity' else None,temperature_c=25 if m=='capacity' else None,retention_threshold=80 if m=='cycle' else None,pic='R&D · Demo') for m,t,u in [('energy',185,'Wh/kg'),('capacity',105,'Ah'),('cycle',2500,'cycles'),('cost_prototype',21.8,'USD/cell'),('cost_sop',18,'USD/cell')]],
        'Energy density':[dict(measurement_id='E001',metric_id='energy',value=None,unit='Wh/kg',discharge_energy_wh=338.2,cell_mass_kg=1.9,condition='0.33C / 25C',c_rate=.33,temperature_c=25,doe_id='DOE-002',build_lot_id='LOT-DEMO-002',cell_id='CELL-DEMO-001',test_date='2026-10-19',approval='Approved',revision='A',pic='Testing · Demo')],
        'Cell capacity':[dict(measurement_id='Q001',metric_id='capacity',value=103.2,unit='Ah',discharge_energy_wh=None,cell_mass_kg=None,condition='0.33C / 25C',c_rate=.33,temperature_c=25,doe_id='DOE-002',build_lot_id='LOT-DEMO-002',cell_id='CELL-DEMO-001',test_date='2026-10-19',approval='Approved',revision='A',pic='Testing · Demo')],
        'Cycle life predicted':[dict(prediction_id='P001',forecast_cycles=2320,retention_threshold=80,model_revision='DEMO-model-A',validated='Yes',condition='0.33C / 25C',doe_id='DOE-002',build_lot_id='LOT-DEMO-002',cell_id='CELL-DEMO-001',prediction_date='2026-10-19',approval='Approved',pic='Data · Demo')],
        'Cell cost Prototype':[dict(line_id='C001',cost_type='Prototype',item='BOM + process ví dụ',quantity=1,unit_price=20,process_cost=2,overhead=.6,currency='USD',approval='Approved',revision='A',updated_at='2026-10-19',pic='Purchasing · Demo')],
        'Cell cost SOP':[dict(line_id='C002',cost_type='SOP',item='BOM + process forecast ví dụ',quantity=1,unit_price=16,process_cost=1.5,overhead=.3,currency='USD',approval='Approved',revision='A',updated_at='2026-10-19',pic='Purchasing · Demo')]},
    }
    for i,(stamp,density) in enumerate([('2026-09-22',163),('2026-09-29',168),('2026-10-06',172),('2026-10-13',175)],2):
        baseline=dict(result['targets']['Energy density'][0],measurement_id=f'E{i:03}',test_date=stamp,discharge_energy_wh=round(density*1.9,4))
        result['targets']['Energy density'].append(baseline)
    result['execution']={'Task Master List':[dict(task_id=f'T{i:02}',title=title,workstream=stream,priority='High',pic=pic+' · Demo',planned_date='2026-10-19',due_date=due,status='In progress',metric=metric,milestone_id='M03',issue_id=issue,doe_id='DOE-002',build_lot_id='LOT-DEMO-002',cell_id='CELL-DEMO-001',description='Task ví dụ cho team thực hành cập nhật sheet.') for i,(title,stream,pic,due,metric,issue) in enumerate([
      ('Review capacity và protocol','Testing','Cell Design','2026-10-25','capacity','I02'),('Review khối lượng và năng lượng','Cell Design','Testing','2026-10-26','energy',None),('Xác nhận mô hình dự đoán','Analysis','Data','2026-10-28','cycle',None),('Review quotation prototype','Cost','Purchasing','2026-11-02','cost_prototype','I04'),('Review SOP forecast','Cost','Purchasing','2026-11-05','cost_sop',None)],1)]}
    curves=[]
    for i in range(21):
        curves.append(dict(record_id=f'CYCLE-{i:03}',series='DEMO · DOE-002',cycle_number=i*50,retention_pct=100-i*.55,voltage=None,discharged_capacity_ah=None,time_s=None,current_a=None,doe_id='DOE-002',cell_id='CELL-DEMO-001',approval='Approved',pic='Testing · Demo'))
        curves.append(dict(record_id=f'DISCH-{i:03}',series='DEMO · 0.33C / 25C',cycle_number=None,retention_pct=None,voltage=round(3.4-.2*i/20-.65*(i/20)**10,4),discharged_capacity_ah=round(103.2*i/20,3),time_s=i*540,current_a=-34.4,doe_id='DOE-002',cell_id='CELL-DEMO-001',approval='Approved',pic='Testing · Demo'))
    result['performance']={'Performance Curves':curves,'Efficiency Inputs':[dict(test_id='EFF-DEMO-001',cell_id='CELL-DEMO-001',doe_id='DOE-002',condition='0.33C / 25C',charge_energy_wh=350,discharge_energy_wh=338.2,charge_capacity_ah=104,discharge_capacity_ah=103.2,test_date='2026-10-19',approval='Approved',pic='Testing · Demo')]}
    result['performance']['DCIR - Impedance']=[dict(test_id='DCIR-DEMO-001',cell_id='CELL-DEMO-001',doe_id='DOE-002',delta_v=-0.02,delta_i=-20,soc_pct=50,temperature_c=25,pulse_window_ms=10000,test_date='2026-10-19',approval='Approved',pic='Testing · Demo')]
    mapping=[dict(cell_id=f'CELL-DEMO-{i:03}',model='52148117',form_factor='Prismatic',diameter_mm=None,height_mm=117,width_mm=148,thickness_mm=52,model_revision='DEMO-A',geometry_ref='Generated geometry · example only',device='TWIN-DEMO-01',channel=f'CH-{i:02}',pic='Digital Twin · Demo') for i in range(1,5)]
    states=[]
    for step in range(13):
        for i in range(1,5):
            states.append(dict(record_id=f'STATE-{i:03}-{step:03}',cell_id=f'CELL-DEMO-{i:03}',timestamp=(datetime.fromisoformat('2026-10-20T09:00:00+07:00')+timedelta(minutes=step*5)).isoformat(),soc_pct=round(20+step*4.5+i*.2,2),voltage_v=round(3.18+step*.018+i*.002,3),current_a=34.4,temperature_c=round(25+step*.45+i*.3,2),cycle_number=35,capacity_ah=103.2-i*.1,retention_pct=98.8-i*.1,status='Charging',pic='Digital Twin · Demo'))
    result['digital_twin']={'Cell Mapping':mapping,'Cell State':states}
    return result

def initialize():
    with store.scope('example'):
        # Do not reset any existing example workbook or user edits.
        data=inputs()
        for key,schema in store.SCHEMAS.items():
            path=store.path_for(EXAMPLE_CELL,key)
            if path.exists():
                with store.lock(EXAMPLE_CELL):store.upgrade(EXAMPLE_CELL,key)
                continue
            sheets=data.get(key,{})
            if key.startswith('function_'):
                sheets={}
                for index,(name,fields) in enumerate(schema['sheets'].items()):
                    if name in schema.get('read_only',[]):
                        sheets[name]=[]
                        continue
                    row={key:None for key in fields}
                    row.update(entry_id=f'DEMO-{index+1:03}',pic='Engineering · Demo',status='Open',revision='A',approval='Draft',doe_id='DOE-002',build_lot_id='LOT-DEMO-002',cell_id='CELL-DEMO-001',notes='Dữ liệu ví dụ, không phải kết quả thử nghiệm.')
                    for field in fields:
                        if field=='material_id':row[field]=f'MAT-DEMO-{index+1:03}'
                        elif field=='supplier':row[field]='Supplier DEMO'
                        elif field=='model':row[field]='52148117'
                        elif field=='chemistry':row[field]='LFP01'
                        elif field=='form_factor':row[field]='Prismatic'
                        elif field=='lot':row[field]='LOT-DEMO-002'
                        elif field=='document_id':row[field]=f'DOC-DEMO-{index+1:03}'
                        elif field=='owner':row[field]='Engineering · Demo'
                    sheets[name]=[row]
            normalized={name:store.normalize(key,name,sheets.get(name,[])) for name in schema['sheets']}
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as handle:handle.write(store.build(key,normalized))
