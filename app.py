"""Workbook-backed Battery R&D application; no synthetic fallbacks in live mode."""
from flask import Flask, jsonify, render_template, request, send_file, abort, Response
import os, hmac
import storage
import workbook_store as store
import example_project
import live_data
from domain import CELLS, MODULES, PROJECTS
from team_folders import TEAMS

storage.initialize()
store.initialize()
example_project.initialize()
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=5*1024*1024

@app.before_request
def request_context():
    dataset=request.args.get('dataset','live')
    if dataset not in ('live','example'):return jsonify(error='Dataset không hợp lệ.'),400
    store.DATASET.set(dataset)
    if dataset=='example' and request.view_args and 'cell' in request.view_args and request.view_args['cell']!=example_project.EXAMPLE_CELL:
        return jsonify(error='Dự án ví dụ chỉ có cell 52148117.'),404
    username=os.environ.get('DASHBOARD_USERNAME');password=os.environ.get('DASHBOARD_PASSWORD')
    if bool(username)!=bool(password):return jsonify(error='Cần cấu hình cả DASHBOARD_USERNAME và DASHBOARD_PASSWORD.'),503
    if username and password:
        auth=request.authorization
        if not auth or not hmac.compare_digest((auth.username or '').encode(),username.encode()) or not hmac.compare_digest((auth.password or '').encode(),password.encode()):
            return Response('Authentication required',401,{'WWW-Authenticate':'Basic realm="Battery R&D", charset="UTF-8"'})
    if request.method in ('POST','PUT','DELETE','PATCH') and request.headers.get('X-Requested-With')!='BatteryDashboard':
        return jsonify(error='Yêu cầu cập nhật không hợp lệ. Hãy lưu từ dashboard.'),403

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['X-Frame-Options']='SAMEORIGIN'
    if request.path.startswith('/api/'):response.headers['Cache-Control']='no-store'
    return response

@app.errorhandler(store.Conflict)
def conflict(error):return jsonify(error=str(error)),409
@app.errorhandler(store.DataError)
def data_error(error):return jsonify(error=str(error)),422
@app.errorhandler(413)
def too_large(error):return jsonify(error='Yêu cầu vượt giới hạn 5 MB.'),413

def valid(cell):
    if cell not in CELLS:abort(404)

@app.get('/')
def index():return render_template('index.html')

@app.get('/api/hierarchy')
def hierarchy():
    return jsonify(projects=PROJECTS,cells=CELLS,teams=TEAMS,modules=[dict(id=n,children=c) for n,c in MODULES],workbooks=[dict(id=key,filename=s['filename'],module=s['module'],section=s['section'],sheets=list(s['sheets'])) for key,s in store.SCHEMAS.items()],example_cell=example_project.EXAMPLE_CELL)

@app.get('/api/programs')
def programs():
    result=[]
    for dataset,cells in [('example',[example_project.EXAMPLE_CELL]),('live',CELLS)]:
        with store.scope(dataset):
            for cell in cells:
                try:
                    data=store.read(cell,'project')['sheets']['Project Information']
                    info=next(iter(data),{})
                except store.DataError:
                    info={'project_name':'Cần kiểm tra workbook Project Information & KPI'}
                result.append(dict(id=dataset+':'+cell,dataset=dataset,cell=cell,code=info.get('project_id') or cell,name=info.get('project_name') or 'Chưa nhập thông tin dự án'))
    return jsonify(programs=result)

@app.get('/api/cells/<cell>/summary')
def summary(cell):valid(cell);return jsonify(live_data.snapshot(cell))

@app.get('/api/cells/<cell>/tasks/<group>')
def task_data(cell,group):
    valid(cell)
    if group not in ('progress','budget','milestones','issues','energy','capacity','cycle','cost','cost_prototype','cost_sop'):abort(404)
    return jsonify(live_data.task_rows(cell,group))

@app.get('/api/cells/<cell>/workbooks/<book>')
def workbook(cell,book):
    valid(cell)
    if book not in store.SCHEMAS:abort(404)
    data=store.read(cell,book)
    data.update(filename=store.SCHEMAS[book]['filename'],fields={name:[dict(name=key,type=kind,required=required,choices=choices) for key,(kind,required,choices) in fields.items()] for name,fields in store.SCHEMAS[book]['sheets'].items()})
    return jsonify(data)

@app.put('/api/cells/<cell>/workbooks/<book>/sheets/<sheet>')
def save_sheet(cell,book,sheet):
    valid(cell)
    if book not in store.SCHEMAS or sheet not in store.SCHEMAS[book]['sheets']:abort(404)
    body=request.get_json(silent=True)
    if not isinstance(body,dict):return jsonify(error='Nội dung phải là JSON.'),400
    result=store.save_sheet(cell,book,sheet,body.get('rows'),body.get('revision'),request.authorization.username if request.authorization else 'local')
    return jsonify(revision=result['revision'],rows=result['sheets'][sheet],modified_at=result['modified_at'])

@app.get('/api/cells/<cell>/workbooks/<book>/download')
def download(cell,book):
    valid(cell)
    if book not in store.SCHEMAS:abort(404)
    # Validation prevents downloading malformed/partly-written files unnoticed.
    store.read(cell,book)
    prefix='EXAMPLE - ' if store.DATASET.get()=='example' else ''
    return send_file(store.path_for(cell,book),as_attachment=True,download_name=prefix+store.SCHEMAS[book]['filename'],mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.get('/api/cells/<cell>/digital-twin')
def digital_twin(cell):
    valid(cell);book=store.read(cell,'digital_twin')
    return jsonify(mapping=book['sheets']['Cell Mapping'],states=book['sheets']['Cell State'],revision=book['revision'],demo=store.DATASET.get()=='example',geometry='parametric',live_connection=False)


@app.get('/api/cycler/state')
def cycler_state():
    if store.DATASET.get()!='example':return jsonify(error='Mô phỏng Cycler chỉ dùng trong dataset ví dụ; không thay dữ liệu thực.'),403
    import cycler_service
    return jsonify(dict(cycler_service.state(),demo=True))

@app.post('/api/cycler/control')
def cycler_control():
    if store.DATASET.get()!='example':return jsonify(error='Không điều khiển mô phỏng từ dataset thực.'),403
    import cycler_service
    try:return jsonify(dict(cycler_service.control(request.get_json(silent=True)),demo=True))
    except ValueError as error:return jsonify(error=str(error)),409

@app.get('/api/cells/<cell>/excel-package')
def excel_package(cell):
    valid(cell)
    import io, zipfile
    output=io.BytesIO()
    with store.lock(cell):
        with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
            for key,schema in store.SCHEMAS.items():
                store.read(cell,key)
                archive.writestr(MODULES[schema['module']][0]+'/'+schema['filename'],store.path_for(cell,key).read_bytes())
            archive.writestr('README.txt',('DỮ LIỆU VÍ DỤ - KHÔNG PHẢI KẾT QUẢ THỰC TẾ.\n' if store.DATASET.get()=='example' else 'DỮ LIỆU DỰ ÁN.\n')+'Mỗi mục chức năng là một workbook. Nội dung con ở trong các sheet. Không thay đổi tên sheet / header. Nhập giá trị, không nhập công thức. Mỗi bản ghi cần ID và PIC. Giữ nguyên lịch sử và raw data.')
    output.seek(0)
    return send_file(output,as_attachment=True,download_name=('EXAMPLE-' if store.DATASET.get()=='example' else '')+cell+'-Excel.zip',mimetype='application/zip')

if __name__=='__main__':app.run(host='0.0.0.0',port=5000,debug=False)
