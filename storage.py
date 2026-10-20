"""Local prototype intake: immutable content-addressed files and SQLite metadata."""
from pathlib import Path
import sqlite3, hashlib, json, re, os
from team_folders import TEAMS
from datetime import datetime, timezone
from domain import CELLS, MODULES
ROOT=Path(__file__).parent/'data'

def safe_folder(label):
    return label.replace(' / ',' - ').replace('/','-')

def connect():
    db=sqlite3.connect(ROOT/'metadata.sqlite3'); db.row_factory=sqlite3.Row
    return db

def initialize():
    (ROOT/'sources').mkdir(parents=True,exist_ok=True)
    for c in CELLS.values():
        for module,children in MODULES:
            parent=ROOT/'projects'/c['project']/c['chemistry']/c['size']/module
            parent.mkdir(parents=True,exist_ok=True)
            # Empty legacy subfolders become sheets; existing files are untouched.
            for child in children:
                legacy=parent/safe_folder(child)
                if legacy.is_dir() and not legacy.is_symlink():
                    try:legacy.rmdir()
                    except OSError:pass
    # Short team folders are relative symlinks, never copies of engineering files.
    for c in CELLS.values():
        team_root=ROOT/'teams'/c['project']/c['chemistry']/c['size']
        team_root.mkdir(parents=True,exist_ok=True)
        for team in TEAMS:
            link=team_root/team['folder']
            target=ROOT/'projects'/c['project']/c['chemistry']/c['size']/MODULES[team['module']][0]
            if not link.exists() and not link.is_symlink():
                link.symlink_to(os.path.relpath(target,link.parent),target_is_directory=True)
    with connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY, cell TEXT NOT NULL,module INTEGER NOT NULL,folder TEXT NOT NULL,filename TEXT NOT NULL,sha256 TEXT NOT NULL,pic TEXT NOT NULL,revision TEXT NOT NULL,doe_id TEXT,build_lot_id TEXT,cell_id TEXT,created_at TEXT NOT NULL, UNIQUE(cell,module,folder,filename,revision))''')

def folder_path(cell,module,folder):
    c=CELLS[cell]
    return ROOT/'projects'/c['project']/c['chemistry']/c['size']/MODULES[module][0]/safe_folder(folder)

def add_document(cell,module,folder,filename,content,meta):
    with connect() as db:
        if db.execute('SELECT id FROM documents WHERE cell=? AND module=? AND folder=? AND filename=? AND revision=?',(cell,module,folder,filename,meta['revision'])).fetchone():
            raise sqlite3.IntegrityError('Revision already exists')
    digest=hashlib.sha256(content).hexdigest()
    # exclusive creation preserves existing source bytes; sources shared by SHA-256
    path=ROOT/'sources'/digest
    try:
        with path.open('xb') as f: f.write(content)
    except FileExistsError:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest: raise ValueError('Source integrity check failed')
    with connect() as db:
        cursor=db.execute('INSERT INTO documents(cell,module,folder,filename,sha256,pic,revision,doe_id,build_lot_id,cell_id,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(cell,module,folder,filename,digest,meta['pic'],meta['revision'],meta.get('doe_id',''),meta.get('build_lot_id',''),meta.get('cell_id',''),datetime.now(timezone.utc).isoformat()))
        ident=cursor.lastrowid
    ref={'document_id':ident,'filename':filename,'sha256':digest,'source':f'sources/{digest}','revision':meta['revision'],'pic':meta['pic']}
    folder_path(cell,module,folder).mkdir(parents=True,exist_ok=True)
    (folder_path(cell,module,folder)/f'{ident:06d}.source.json').write_text(json.dumps(ref,ensure_ascii=False,indent=2))
    return ident

def document_rows(cell,module):
    with connect() as db: docs=db.execute('SELECT * FROM documents WHERE cell=? AND module=? ORDER BY id DESC',(cell,module)).fetchall()
    return [dict(id=f"DOC-{d['id']}",content=d['folder'],information=f"{d['filename']} · Rev {d['revision']}",source_id=f"DOC-{d['id']}",source_path=f"/api/documents/{d['id']}",pic=d['pic'],status='In review',revision=d['revision'],approval='Pending review',doe_id=d['doe_id'],build_lot_id=d['build_lot_id'],cell_id=d['cell_id'],demo=False,filename=d['filename'],sha256=d['sha256']) for d in docs]
