"""Real summaries from validated workbook inputs. Missing information stays null."""
from datetime import datetime, date
from zoneinfo import ZoneInfo
from decimal import Decimal
import hashlib
import workbook_store as store
from catalog import source_link, warning_color

METRICS={'energy':('Energy density','Wh/kg'),'capacity':('Cell capacity','Ah'),'cycle':('Cycle life (dự đoán)','cycles'),'cost_prototype':('Cell cost — Prototype','USD/cell'),'cost_sop':('Cell cost — SOP','USD/cell')}

def total(rows,key):
    return float(sum((Decimal(str(r[key])) for r in rows),Decimal(0))) if rows and all(r.get(key) is not None for r in rows) else None

def snapshot(cell,books=None):
    if books is None:
      with store.lock(cell):
        books={key:store.read(cell,key) for key in ('project','timeline','issues','execution','targets','doe_runs','performance')}
    sheets=lambda key,name:books[key]['sheets'][name]
    info=next(iter(sheets('project','Project Information')), {})
    milestones=[r for r in sheets('timeline','Project Milestones') if r['status']!='Cancelled']
    weights=sum(r['weight'] for r in milestones)
    progress=round(sum(r['weight']*r['completion'] for r in milestones)/weights,2) if weights else None
    completed=[r for r in milestones if r['status'] in ('Completed','Approved')]
    budgets=sheets('project','Budget');currencies={r['currency'] for r in budgets}
    warnings=[]
    currency=info.get('currency') or (next(iter(currencies)) if len(currencies)==1 else None)
    budget={k:total(budgets,k) if len(currencies)<=1 and (not currencies or currency in currencies) else None for k in ('approved','actual','committed','forecast')}
    if len(currencies)>1 or (currencies and currency not in currencies):warnings.append('Ngân sách có nhiều currency hoặc không khớp Project Information; không cộng gộp tiền tệ.')
    budget['currency']=currency
    budget['remaining']=round(budget['approved']-budget['actual']-budget['committed'],8) if all(budget[k] is not None for k in ('approved','actual','committed')) else None
    today=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).date().isoformat()
    issues=[dict(r) for r in sheets('issues','Issue Register')];open_issues=[r for r in issues if r['status']!='Closed']
    for row in issues:row['color']=warning_color(row['severity'],bool(row['due_date'] and row['due_date']<today and row['status']!='Closed'),row['severity']=='High')
    project_color='Red' if any(r['color']=='Red' for r in open_issues) else 'Amber' if any(r['color']=='Amber' for r in open_issues) or any(r['status']=='Blocked' or (r['baseline'] and (r['forecast'] or r['actual'] or today)>r['baseline'] and r['status'] not in ('Completed','Approved')) for r in milestones) else 'Green' if milestones or issues else 'Grey'
    runs=[r for r in sheets('doe_runs','DOE Runs') if r['status']!='Cancelled']
    doe_completed=sum(r['status'] in ('Completed','Approved') for r in runs)
    tasks=sheets('execution','Task Master List')
    target_map={r['metric_id']:r for r in sheets('targets','Targets')}
    metrics={}
    for key,(label,unit) in METRICS.items():
        target=target_map.get(key)
        metric=dict(id=key,label=label,unit=target['unit'] if target else unit,target=target['target'] if target else None,actual=None,pass_status=None,approved_count=0,condition=target.get('condition') if target else None,predicted=key=='cycle',warning=None)
        if key in ('energy','capacity'):
            candidates=[r for r in sheets('targets','Energy density' if key=='energy' else 'Cell capacity') if r['approval']=='Approved']
            candidates=match_conditions(candidates,target,key)
            if candidates is None:metric['warning']='Chọn condition / DOE và điều kiện thử trong Targets trước khi so sánh các tập dữ liệu khác điều kiện.';candidates=[]
            if candidates:
                latest=max(r['test_date'] for r in candidates);chosen=[r for r in candidates if r['test_date']==latest]
                metric['actual']=sum(r['discharge_energy_wh'] for r in chosen)/sum(r['cell_mass_kg'] for r in chosen) if key=='energy' else sum(r['value'] for r in chosen)/len(chosen)
                metric['approved_count']=len(chosen);metric['date']=latest
        elif key=='cycle':
            candidates=[r for r in sheets('targets','Cycle life predicted') if r['approval']=='Approved' and r['validated']=='Yes']
            candidates=match_conditions(candidates,target,key)
            if candidates is None:candidates=[];metric['warning']='Chọn condition / DOE cho mô hình dự đoán.'
            if not target or target['retention_threshold'] is None:candidates=[]
            else:candidates=[r for r in candidates if r['retention_threshold']==target['retention_threshold']]
            if candidates:
                latest=max(r['prediction_date'] for r in candidates);chosen=[r for r in candidates if r['prediction_date']==latest]
                if len(chosen)==1:
                    metric['actual']=chosen[0]['forecast_cycles'];metric['model_revision']=chosen[0]['model_revision'];metric['date']=latest;metric['approved_count']=1
                else:metric['warning']='Có nhiều dự đoán approved cùng ngày; cần chọn một mô hình để tránh lấy tùy ý.'
        else:
            candidates=[r for r in sheets('targets','Cell cost Prototype' if key=='cost_prototype' else 'Cell cost SOP') if r['approval']=='Approved']
            codes={r['currency'] for r in candidates};expected=target['unit'].split('/')[0] if target else None
            if candidates and len(codes)==1 and (not expected or expected in codes):
                metric['actual']=float(sum((Decimal(str(r['quantity']))*Decimal(str(r['unit_price']))+Decimal(str(r['process_cost'] or 0))+Decimal(str(r['overhead'] or 0)) for r in candidates),Decimal(0)))
                metric['unit']=next(iter(codes))+'/cell';metric['approved_count']=len(candidates)
            elif candidates:metric['warning']='Currency của các dòng chi phí không đồng nhất hoặc không khớp target; không quy đổi tự động.'
        if metric['actual'] is not None:metric['actual']=round(metric['actual'],8)
        if metric['target'] is not None and metric['actual'] is not None:metric['pass_status']=metric['actual']<=metric['target'] if key.startswith('cost_') else metric['actual']>=metric['target']
        metrics[key]=metric
    upcoming=sorted([dict(r,delta_days=(date.fromisoformat(r['forecast'])-date.fromisoformat(r['baseline'])).days if r['forecast'] and r['baseline'] else None) for r in milestones if r['status'] not in ('Completed','Approved')],key=lambda r:r['forecast'] or r['baseline'] or '9999')
    points=sheets('performance','Performance Curves')
    revision=hashlib.sha256(''.join(b['revision'] for b in books.values()).encode()).hexdigest()
    return dict(cell=cell,info=info,progress=progress,budget=budget,milestones=dict(completed=len(completed),total=len(milestones),upcoming=upcoming),issues=dict(open=len(open_issues),overdue=sum(bool(r['due_date'] and r['due_date']<today) for r in open_issues),critical=sum(r['severity']=='Critical' for r in open_issues),rows=open_issues),doe=dict(total=len(runs),completed=doe_completed,progress=round(doe_completed/len(runs)*100,2) if runs else None),color=project_color,metrics=metrics,tasks=tasks,charts=dict(energy=[r for r in sheets('targets','Energy density') if r['approval']=='Approved'],curves=[r for r in points if r['approval']=='Approved']),warnings=warnings,revision=revision,updated_at=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(),demo=store.DATASET.get()=='example')

def match_conditions(rows,target,key):
    for field in ('condition','doe_id')+ (('c_rate','temperature_c') if key=='capacity' else ()):
        value=target.get(field) if target else None
        if value is not None:rows=[r for r in rows if r.get(field)==value]
        elif len({r.get(field) for r in rows})>1:return None
    return rows

def task_rows(cell,group):
    live=snapshot(cell)
    source=source_link(group if group not in ('cost_prototype','cost_sop') else 'cost')
    if group=='milestones':
        rows=store.read(cell,'timeline')['sheets']['Project Milestones'];title='Milestones'
        result=[dict(id=r['milestone_id'],content=r['name'],information=f"Baseline: {r['baseline'] or '—'} · Forecast: {r['forecast'] or '—'} · Actual: {r['actual'] or '—'} · Completion: {r['completion']}%",pic=r['pic'],due=r['forecast'] or r['baseline'],status=r['status']) for r in rows if r['status']!='Cancelled']
    elif group=='issues':
        result=[dict(id=r['issue_id'],content=r['title'],information=r['action'] or '',pic=r['pic'],due=r['due_date'],status=r['status'],severity=r['severity'],color=r['color']) for r in live['issues']['rows']];title='Issues đang mở'
    else:
        all_tasks=live['tasks'];title={'progress':'Tiến độ dự án','budget':'Ngân sách'}.get(group,METRICS.get(group,('Cell cost',))[0])
        selected=all_tasks if group=='progress' else [r for r in all_tasks if ('cost' in (r['workstream'] or '').lower() if group=='budget' else r['metric'] in ('cost_prototype','cost_sop') if group=='cost' else r['metric']==group)]
        result=[dict(id=r['task_id'],content=r['title'],information=r['description'] or '',pic=r['pic'],due=r['due_date'],status=r['status'],doe_id=r['doe_id'],build_lot_id=r['build_lot_id'],cell_id=r['cell_id']) for r in selected]
    for r in result:r['demo']=store.DATASET.get()=='example'
    return dict(rows=result,title=title,source=source,module=source['module'],value=None,description='Công việc từ các sheet đã lưu, theo cell đang chọn.',demo=store.DATASET.get()=='example')
