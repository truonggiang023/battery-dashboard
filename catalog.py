"""User-provided content specification, separate from synthetic task results."""
import json
from pathlib import Path
CATALOG=json.loads((Path(__file__).parent/'configuration/content_catalog.json').read_text())

def content_rows(cell,module):
    return [dict(r,id=f"{cell}-{r['id']}",source_id=r['id'],status='Chưa kết nối',definition=True,demo=True,doe_id='',build_lot_id='',cell_id=cell) for r in CATALOG['records'] if r['module']==module]

def warning_color(severity='',overdue=False,high=False,has_data=True):
    if not has_data:return 'Grey'
    if severity.lower()=='critical':return 'Red'
    if overdue or high:return 'Amber'
    return 'Green'

SOURCE_LINKS={
 'progress':dict(spec='Tiến độ dự án (%)',destination='Master Timeline',module=0,section='Master Timeline'),
 'budget':dict(spec='Ngân sách',destination='Cost Analysis',module=7,section='BOM & Cost'),
 'milestones':dict(spec='Milestones hoàn thành',destination='Master Timeline',module=0,section='Master Timeline'),
 'issues':dict(spec='Issues đang mở',destination='Issue Register',module=0,section='Rủi ro & Sự vụ'),
 'energy':dict(spec='Energy density (Wh/kg)',destination='Electrical Performance',module=6,section='Electrical Performance'),
 'capacity':dict(spec='Cell capacity (Ah)',destination='Capacity Results',module=5,section='Test Categories'),
 'cycle':dict(spec='Cycle life predicted',destination='Cycling',module=6,section='Cycle Life Analysis'),
 'cost':dict(spec='Cell cost — Prototype / SOP',destination='Cost Analysis',module=7,section='BOM & Cost'),
}

def source_link(group):
    link=SOURCE_LINKS[group]
    definition=next(r for r in CATALOG['records'] if r['content']==link['spec'])
    return dict(**link,information=definition['information'],source_path=definition['source_path'],calculation=definition['calculation'],pic=definition['pic'])
