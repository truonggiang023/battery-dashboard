import unittest, tempfile, io, csv
from pathlib import Path
import storage
from app import app
from domain import CELLS, MODULES

class DashboardTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.original=storage.ROOT
        storage.ROOT=Path(self.tmp.name); storage.initialize()
        self.client=app.test_client()
    def tearDown(self):
        storage.ROOT=self.original; self.tmp.cleanup()
    def upload(self,revision='A',cell='CYL-LFP-40135'):
        return self.client.post('/api/intake',data={'cell':cell,'module':'2','folder':'Cathode','pic':'Materials team','revision':revision,'doe_id':'DOE-TEST','file':(io.BytesIO(b'test,value\ncapacity,10\n'),'sample.csv')})
    def test_all_cells_have_exact_standard_structure(self):
        for cell in CELLS:
            for i,(_,children) in enumerate(MODULES):
                for child in children: self.assertTrue(storage.folder_path(cell,i,child).is_dir())
        h=self.client.get('/api/hierarchy').json
        self.assertEqual(len(h['cells']),5)
        self.assertEqual(h['projects'][1]['chemistries'][1]['sizes'],[])
    def test_intake_revision_integrity_and_cell_isolation(self):
        response=self.upload(); self.assertEqual(response.status_code,201)
        ident=response.json['id']
        with self.client.get(f'/api/documents/{ident}') as download: original=download.data
        self.assertEqual(original,b'test,value\ncapacity,10\n')
        self.assertEqual(self.upload().status_code,409)
        self.assertEqual(self.upload('B').status_code,201)
        self.assertEqual(len(list((storage.ROOT/'sources').iterdir())),1)
        rows=self.client.get('/api/cells/CYL-LFP-40135/modules/2?q=sample.csv').json['rows']
        self.assertEqual(len(rows),2)
        self.assertEqual(self.client.get('/api/cells/CYL-LFP-21700/modules/2?q=sample.csv').json['rows'],[])
        with self.client.get(f'/api/documents/{ident}') as download: self.assertEqual(download.data,original)
        export=self.client.get('/api/export/CYL-LFP-40135/2')
        self.assertEqual(export.status_code,200)
        self.assertEqual(len(list(csv.DictReader(io.StringIO(export.text)))),8)
    def test_validation_and_readonly_preview(self):
        self.assertEqual(self.client.post('/api/intake',data={'cell':'../escape'}).status_code,400)
        result=self.client.post('/api/preview',data={'file':(io.BytesIO(b'a,b\n1,2'),'x.csv')})
        self.assertEqual(result.status_code,200); self.assertIn('1 | 2',result.json['preview'])
        self.assertEqual(list((storage.ROOT/'sources').iterdir()),[])
        self.assertEqual(self.client.get('/api/cells/unknown/modules/0').status_code,404)
    def test_overview_task_links_are_scoped_to_selected_cell(self):
        for group in ('progress','budget','milestones','issues','energy','capacity','cycle','cost'):
            response=self.client.get(f'/api/cells/CYL-LFP-40135/tasks/{group}')
            self.assertEqual(response.status_code,200)
            rows=response.json['rows']; self.assertTrue(rows)
            self.assertTrue(all(row['id'].startswith('CYL-LFP-40135-') and row['pic'] and row['due'] and row['demo'] for row in rows))
        other=self.client.get('/api/cells/CYL-SIB-21700/tasks/capacity').json['rows']
        self.assertTrue(all(row['id'].startswith('CYL-SIB-21700-') for row in other))
        self.assertEqual(self.client.get('/api/cells/unknown/tasks/energy').status_code,404)
        self.assertEqual(self.client.get('/api/cells/CYL-LFP-40135/tasks/unknown').status_code,404)

    def test_team_links_and_content_contract(self):
        from team_folders import TEAMS
        from catalog import CATALOG
        for c in CELLS.values():
            for team in TEAMS:
                short=storage.ROOT/'teams'/c['project']/c['chemistry']/c['size']/team['folder']
                target=storage.ROOT/'projects'/c['project']/c['chemistry']/c['size']/MODULES[team['module']][0]
                self.assertTrue(short.is_symlink())
                self.assertEqual(short.resolve(),target.resolve())
        actual=[]
        for module in range(10):
            response=self.client.get(f'/api/cells/CYL-LFP-40135/content/{module}')
            self.assertEqual(response.status_code,200)
            self.assertFalse(response.json['connected'])
            actual.extend(response.json['rows'])
        self.assertEqual(len(actual),len(CATALOG['records']))
        self.assertTrue(all(r['definition'] and r['status']=='Chưa kết nối' for r in actual))
        self.assertTrue(any('Σ(Weight × completion)/ΣWeight' in r['calculation'] for r in actual))
        self.assertEqual(self.client.get('/api/cells/unknown/content/0').status_code,404)

    def test_filters(self):
        rows=self.client.get('/api/cells/CYL-LFP-40135/modules/0?status=Approved').json['rows']
        self.assertTrue(rows); self.assertTrue(all(r['status']=='Approved' for r in rows))

if __name__=='__main__': unittest.main()
