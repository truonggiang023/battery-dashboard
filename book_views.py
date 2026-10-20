"""Materialized read-only content sheets, calculated from canonical inputs.

Each function owns its requested tabs. Summary tabs never become a second
editable copy of milestone, issue or measurement records.
"""
from datetime import date, datetime
from zoneinfo import ZoneInfo
import workbook_store as store
import live_data


def number(value):return '—' if value is None else f'{value:g}'
def row(ident,content,information='',pic='',status=''):
    ident=str(ident)
    if len(ident)>1800:
        import hashlib
        ident='ID-'+hashlib.sha256(ident.encode()).hexdigest()
    information=str(information)
    if len(information)>2000:information=information[:1999]+'…'
    return dict(record_id=ident,content=str(content),information=information,pic=pic or '',status=status or '')

def calculate(cell,books):
    live=live_data.snapshot(cell,books)
    source=lambda book,sheet:books[book]['sheets'][sheet]
    milestones=source('timeline','Project Milestones');tasks=source('execution','Task Master List')
    today=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).date().isoformat()
    result={key:{} for key,schema in store.SCHEMAS.items() if schema.get('read_only')}
    n=store.sheet_name
    progress=live['progress'];gates=live['milestones'];issues=live['issues']
    result['project'][n('Tiến độ dự án (%)')]=[row('PROGRESS','Tiến độ dự án (%)',number(progress)+'%' if progress is not None else 'Chưa có weighted milestones.','PMO','Chưa có dữ liệu' if progress is None else 'Calculated')]
    result['project'][n('Milestones hoàn thành')]=[row('GATES','Milestones hoàn thành',f"{gates['completed']}/{gates['total']} gates Completed / Approved" if gates['total'] else 'Chưa có milestones.','PMO','Calculated' if gates['total'] else 'Chưa có dữ liệu')]
    result['project'][n('Issues đang mở')]=[row(r['issue_id'],r['title'],f"{r['severity']} · Due: {r['due_date'] or '—'} · {r['action'] or ''}",r['pic'],r['status']) for r in issues['rows']]
    cost=[]
    for key in ('cost_prototype','cost_sop'):
        metric=live['metrics'][key]
        cost.append(row(key,metric['label'],f"Actual: {number(metric['actual'])}; Target: {number(metric['target'])} {metric['unit']}",'PMO','Chưa đủ dữ liệu' if metric['pass_status'] is None else 'Đạt' if metric['pass_status'] else 'Chưa đạt'))
    result['targets']['Cell cost - Prototype - SOP']=cost
    phase_key=next(key for key,s in store.SCHEMAS.items() if s['section']=='Project Status' and s['module']==0)
    approved=sorted([r for r in milestones if r['status']=='Approved' and r['actual']],key=lambda r:r['actual'])
    phase=live['info'].get('phase') or (approved[-1]['name'] if approved else None)
    result[phase_key][n('Current Phase / Stage Gate')]=[row('PHASE','Current Phase / Stage Gate',phase or 'Chưa có phase / approved gate.','PMO','Recorded' if phase else 'Chưa có dữ liệu')]
    doe=live['doe']
    result[phase_key][n('DOE progress')]=[row('DOE','DOE progress',f"{doe['completed']}/{doe['total']} valid runs · {number(doe['progress'])}%" if doe['total'] else 'Chưa có DOE runs.','Cell Design','Calculated' if doe['total'] else 'Chưa có dữ liệu')]
    result[phase_key][n('Milestones tiếp theo')]=[row(r['milestone_id'],r['name'],f"Baseline: {r['baseline'] or '—'}; Forecast: {r['forecast'] or '—'}; Δdays: {r['delta_days'] if r['delta_days'] is not None else '—'}",r['pic'],r['status']) for r in gates['upcoming']]
    result[phase_key][n('Project warning colors')]=[row('PROJECT-COLOR','Project warning colors',f"{live['color']} · {issues['critical']} critical, {issues['overdue']} overdue issues. Critical → Red; overdue/high → Amber; normal → Green; no data → Grey.",'PMO',live['color'])]
    pending=[]
    for sheet in ('Task Master List','Action Tracking'):
        for r in source('execution',sheet):
            if r['status'] in ('Completed','Closed','Cancelled'):continue
            overdue=(date.fromisoformat(today)-date.fromisoformat(r['due_date'])).days if r['due_date'] and r['due_date']<today else 0
            pending.append(row(sheet+':'+r['task_id'],r['title'],f"Due: {r['due_date'] or '—'}; overdue: {overdue} days; {r['description'] or ''}",r['pic'],'Overdue' if overdue else r['status']))
    result['execution'][n('Pending / Overdue')]=pending
    result['timeline']['Gantt Chart']=[row(r['task_id'],r['title'],f"Start: {r['planned_date']}; End: {r['due_date']}; milestone: {r['milestone_id'] or '—'}",r['pic'],r['status']) for r in tasks if r['planned_date'] and r['due_date']]
    variation=[]
    for r in milestones:
        latest=r['actual'] or r['forecast']
        delta=(date.fromisoformat(latest)-date.fromisoformat(r['baseline'])).days if latest and r['baseline'] else None
        variation.append(row(r['milestone_id'],r['name'],f"Baseline: {r['baseline'] or '—'}; Forecast: {r['forecast'] or '—'}; Actual: {r['actual'] or '—'}; Δdays: {delta if delta is not None else '—'}",r['pic'],r['status']))
    result['timeline']['Planned vs Actual']=variation
    result['timeline']['Critical Activities']=[row('TASK:'+r['task_id'],r['title'],'PMO priority flag: Critical (không tự tính critical path/CPM).',r['pic'],r['status']) for r in tasks if r['priority']=='Critical' and r['status'] not in ('Completed','Closed','Cancelled')]+[row('GATE:'+r['milestone_id'],r['name'],f"Blocked gate; depends_on: {r['depends_on'] or '—'} (không tự tính CPM).",r['pic'],r['status']) for r in milestones if r['status']=='Blocked']
    capacity=[r for r in source('targets','Cell capacity') if r['approval']=='Approved']
    result['performance']['Capacity Test']=[row(r['measurement_id'],r['cell_id'] or r['measurement_id'],f"{number(r['value'])} Ah · {number(r['c_rate'])}C · {number(r['temperature_c'])}°C · {r['test_date']} · DOE: {r['doe_id'] or '—'}",r['pic'],r['approval']) for r in capacity]
    efficiency=[r for r in source('performance','Efficiency Inputs') if r['approval']=='Approved']
    result['performance'][n('Energy / Efficiency')]=[row(r['test_id'],r['cell_id'],f"Echarge: {number(r['charge_energy_wh'])} Wh; Edischarge: {number(r['discharge_energy_wh'])} Wh; CE: {r['discharge_capacity_ah']/r['charge_capacity_ah']*100:.4f}%; EE: {r['discharge_energy_wh']/r['charge_energy_wh']*100:.4f}%; condition: {r['condition'] or '—'}",r['pic'],r['approval']) for r in efficiency]
    curves=[r for r in source('performance','Performance Curves') if r['approval']=='Approved' and r['voltage'] is not None]
    result['performance']['Voltage Curves']=[row(r['record_id'],r['series'],f"Cell: {r['cell_id'] or '—'}; Q: {number(r['discharged_capacity_ah'])} Ah; V: {number(r['voltage'])}; t: {number(r['time_s'])} s; I: {number(r['current_a'])} A",r['pic'],r['approval']) for r in curves]
    energy=[r for r in source('targets','Energy density') if r['approval']=='Approved']
    result['performance']['Energy Density']=[row(r['measurement_id'],r['cell_id'] or r['measurement_id'],f"{r['discharge_energy_wh']/r['cell_mass_kg']:.4f} Wh/kg = {number(r['discharge_energy_wh'])} Wh / {number(r['cell_mass_kg'])} kg · {r['test_date']} · DOE: {r['doe_id'] or '—'}",r['pic'],r['approval']) for r in energy]
    return result


def refresh(cell):
    """Recalculate only changed views; input cells and all older files survive."""
    with store.lock(cell):
        required=set(('project','timeline','issues','execution','targets','doe_runs','performance'))
        required.update(key for key,schema in store.SCHEMAS.items() if schema.get('read_only'))
        books={key:store.read(cell,key) for key in required}
        views=calculate(cell,books)
        for key,sheets in views.items():
            current=books[key];changed=False
            for name,records in sheets.items():
                records=store.normalize(key,name,records)
                if current['sheets'][name]!=records:current['sheets'][name]=records;changed=True
            if changed:
                store.replace_content(cell,key,store.build(key,current['sheets']),current['revision'],'system','refresh_views',', '.join(sheets))
