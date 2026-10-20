from flask import Flask, jsonify, render_template, request, Response, abort
from domain import MODULES, PROJECTS, CELLS, records
import csv, io, sqlite3
from pathlib import Path
from flask import send_file
import storage
storage.initialize()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/api/hierarchy')
def hierarchy():
    return jsonify(projects=PROJECTS, modules=[dict(id=n,children=c) for n,c in MODULES],cells=CELLS,demo=True)

@app.get('/api/cells/<cell_id>/modules/<int:module>')
def module_data(cell_id,module):
    if cell_id not in CELLS or not 0 <= module < len(MODULES): abort(404)
    rows=storage.document_rows(cell_id,module)+records(cell_id,module)
    status=request.args.get('status','')
    q=request.args.get('q','').lower()
    rows=[r for r in rows if (not status or r['status']==status) and (not q or q in ' '.join(str(v) for v in r.values()).lower())]
    return jsonify(rows=rows,demo=True,cell=CELLS[cell_id])

@app.get('/api/export/<cell_id>/<int:module>')
def export(cell_id,module):
    if cell_id not in CELLS or not 0 <= module < len(MODULES): abort(404)
    rows=storage.document_rows(cell_id,module)+records(cell_id,module); output=io.StringIO()
    writer=csv.DictWriter(output,fieldnames=list(dict.fromkeys(k for row in rows for k in row))); writer.writeheader(); writer.writerows(rows)
    return Response(output.getvalue(),mimetype='text/csv',headers={'Content-Disposition':f'attachment; filename="DEMO-{cell_id}-{module}.csv"'})

@app.errorhandler(413)
def too_large(error):
    return jsonify(error='File quá lớn. Giới hạn 5 MB.'),413

@app.post('/api/intake')
def intake():
    cell=request.form.get('cell',''); module=request.form.get('module',type=int); folder=request.form.get('folder','')
    if cell not in CELLS or module is None or not 0 <= module < len(MODULES) or folder not in MODULES[module][1]:
        return jsonify(error='Chọn đúng Project → Chemistry → Cell Size → thư mục.'),400
    meta={k:request.form.get(k,'').strip() for k in ('pic','revision','doe_id','build_lot_id','cell_id')}
    if not meta['pic'] or not meta['revision']: return jsonify(error='PIC và revision là bắt buộc.'),400
    if any(len(v)>200 for v in meta.values()): return jsonify(error='Metadata tối đa 200 ký tự mỗi trường.'),400
    file=request.files.get('file')
    allowed={'.csv','.xlsx','.pdf','.step','.stp','.txt','.json','.png','.jpg','.jpeg'}
    if not file or not file.filename or Path(file.filename).suffix.lower() not in allowed:
        return jsonify(error='Định dạng hỗ trợ: CSV, XLSX, PDF, STEP, TXT, JSON, PNG, JPG.'),400
    name=Path(file.filename.replace('\\','/')).name[:200]
    content=file.read()
    if not content: return jsonify(error='File rỗng.'),400
    try: ident=storage.add_document(cell,module,folder,name,content,meta)
    except sqlite3.IntegrityError: return jsonify(error='Revision đã tồn tại cho file trong thư mục này. Hãy dùng revision mới.'),409
    return jsonify(id=ident,message='Đã lưu file gốc và liên kết vào thư mục. Chờ review.'),201

@app.get('/api/documents/<int:ident>')
def document(ident):
    with storage.connect() as db: row=db.execute('SELECT * FROM documents WHERE id=?',(ident,)).fetchone()
    if row is None: abort(404)
    return send_file(storage.ROOT/'sources'/row['sha256'],as_attachment=True,download_name=row['filename'],mimetype='application/octet-stream')

@app.post('/api/preview')
def preview():
    file=request.files.get('file')
    if not file: return jsonify(error='Choose a file.'),400
    suffix=Path(file.filename or '').suffix.lower()
    try:
        if suffix=='.csv':
            reader=csv.reader(io.StringIO(file.read().decode('utf-8-sig')))
            import itertools
            text='\n'.join(' | '.join(row[:20]) for row in itertools.islice(reader,20))[:20000]
        elif suffix=='.xlsx':
            import openpyxl, zipfile
            content=io.BytesIO(file.read())
            with zipfile.ZipFile(content) as archive:
                if sum(i.file_size for i in archive.infolist())>30_000_000: return jsonify(error='Workbook expands beyond preview limit.'),400
            content.seek(0)
            wb=openpyxl.load_workbook(content,read_only=True,data_only=True)
            text='\n'.join(' | '.join(str(v or '') for v in row) for row in wb.active.iter_rows(max_row=20,max_col=20,values_only=True))[:20000]
            wb.close()
        elif suffix=='.pdf':
            from pypdf import PdfReader
            reader=PdfReader(file.stream)
            text='\n'.join(page.extract_text() or '[No selectable text on this page]' for page in reader.pages[:2])[:20000]
        else: return jsonify(error='Preview supports CSV, XLSX and PDF text only.'),400
        return jsonify(preview=text or '[Empty document]')
    except Exception:
        return jsonify(error='Cannot parse this file. Check its format, encoding or encryption.'),400

if __name__ == '__main__': app.run(host='0.0.0.0',port=5000,debug=False)
