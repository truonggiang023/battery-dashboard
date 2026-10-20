"""Rack model adapted from truonggiang023/Digital-Twin @ 1b999d1."""
import threading, uuid
from .model import Battery, simulate
from .live_features import EarlyDischargeWindow
from .ml_inference import predict as ml_predict

class Rack:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        self.session_id=uuid.uuid4().hex
        self.running = False
        self.speed = 60
        self.fraction = 0.0
        self.cells = []
        self.streams = []
        self.batteries = []
        self.alarms = []
        self.safety_stop = False
        self.pending_fault = None
        self.live_windows = [EarlyDischargeWindow() for _ in range(12)]
        self.discharge_starts = [None]*12
        self.previous_stages = ['ready']*12
        self.previous_times = [0.0]*12
        for i in range(12):
            battery = Battery(capacity_ah=2.5 + 0.025 * i,
                              resistance_ohm=0.07 + 0.004 * i,
                              soc=0.15 + 0.025 * i,
                              temperature_c=25 + 0.2 * i, ambient_c=25 + 0.2 * i)
            self.streams.append(simulate(battery, cycles=3, current_a=2, dt_s=1))
            self.batteries.append(battery)
            self.cells.append(dict(id=i + 1, form_factor='PRISMATIC' if i<6 else 'CYLINDRICAL',
                                   project_id='prismatic-lfp01' if i<6 else 'cylindrical-lfp01', doe_name='DOE-P-LFP01' if i<6 else 'DOE-C-LFP01', cell_name=('DOE-P-LFP01' if i<6 else 'DOE-C-LFP01')+'-C%02d'%(i%6+1), time_s=0, cycle=1, stage='ready', mode='READY',
                                   voltage_v=battery.ocv, current_a=0, soc=battery.soc,
                                   temperature_c=battery.temperature_c, stage_capacity_ah=0,
                                   status='ready', error='', live_ml=self.waiting_prediction(),
                                   live_ml_history=[],live_soh_history=[dict(time_s=0,simulated_soh_percent=100)], **battery.health()))

    @staticmethod
    def waiting_prediction():
        return dict(status='waiting',remaining_cycles=None,soh_percent=None,
                    feature_cycle=None,updated_time_s=None,sample_count=0,
                    window_s=600,experimental=True,valid_for_hardware=False,
                    reason='Waiting for 600 seconds of discharge telemetry')

    def collect_prediction(self,index):
        cell=self.cells[index]
        stage=cell['stage']
        if cell['time_s']-cell['live_soh_history'][-1]['time_s']>=30:
            cell['live_soh_history'].append(dict(time_s=cell['time_s'],simulated_soh_percent=cell['soh_percent']))
            cell['live_soh_history']=cell['live_soh_history'][-2048:]
        if stage=='discharge':
            if self.previous_stages[index]!='discharge':
                self.discharge_starts[index]=self.previous_times[index]
                if cell['live_ml']['feature_cycle']!=cell['cycle']:
                    cell['live_ml']['status']='collecting'
            try:
                features=self.live_windows[index].add(
                    cycle=cell['cycle'],stage=stage,time_s=cell['time_s'],
                    voltage_v=cell['voltage_v'],current_a=cell['current_a'],
                    temperature_c=cell['temperature_c'],
                    ambient_temperature_c=self.batteries[index].ambient_c,
                    stage_start_s=self.discharge_starts[index])
                window=self.live_windows[index]
                cell['live_ml']['sample_count']=window.count
                if features:
                    prediction=ml_predict(features)
                    cell['live_ml']=dict(**prediction,status='ready',experimental=True,
                                         valid_for_hardware=False,feature_cycle=cell['cycle'],
                                         updated_time_s=cell['time_s'],sample_count=window.count,
                                         window_s=600,features=features,
                                         reason='NASA-trained model applied to simulated signals; not calibrated')
                    cell['live_ml_history'].append(dict(cycle=cell['cycle'],time_s=cell['time_s'],
                                                       soh_percent=prediction['soh_percent'],
                                                       simulated_soh_percent=cell['soh_percent'],
                                                       remaining_cycles=prediction['remaining_cycles']))
                    cell['live_ml_history']=cell['live_ml_history'][-200:]
                elif window.error:
                    cell['live_ml'].update(status='insufficient',reason=window.error)
            except (ValueError,OSError) as error:
                cell['live_ml'].update(status='error',reason=str(error))
        elif self.previous_stages[index]=='discharge' and not self.live_windows[index].ready:
            cell['live_ml'].update(status='insufficient',reason='Discharge ended before a complete 600-second window')
        self.previous_stages[index]=stage
        self.previous_times[index]=cell['time_s']

    def tick(self, wall_dt):
        if not self.running:
            return
        self.fraction += min(wall_dt, 0.5) * self.speed
        steps = int(self.fraction)
        self.fraction -= steps
        for _ in range(steps):
            for index, (cell, stream) in enumerate(zip(self.cells, self.streams)):
                if cell['status'] in ('complete', 'fault'):
                    continue
                try:
                    cell.update(next(stream), status='running')
                except StopIteration:
                    cell.update(status='complete', current_a=0)
                except RuntimeError as error:
                    self.trip(cell, str(error))
                    return
                if self.pending_fault and self.pending_fault['cell']==index+1:
                    kind=self.pending_fault['kind']
                    if kind=='overheat':cell['temperature_c']=50
                    elif kind=='overvoltage':cell['voltage_v']=4.5
                    elif kind=='overcurrent':cell['current_a']=8
                    elif kind=='capacity_drop':
                        self.batteries[index].aging_damage+=0.5
                        cell.update(self.batteries[index].health())
                    self.pending_fault=None
                reason=None
                if cell['temperature_c']>=45:reason='Quá nhiệt: ≥45 °C'
                elif cell['voltage_v']>4.2+1e-5 or cell['voltage_v']<3-1e-5:reason='Điện áp ngoài giới hạn 3.0–4.2 V'
                elif abs(cell['current_a'])>2.2:reason='Quá dòng: >2.2 A'
                elif cell['soh_percent']<80:reason='SOH dưới ngưỡng an toàn 80%'
                if reason:
                    self.trip(cell,reason)
                    return
                self.collect_prediction(index)
        if all(c['status'] in ('complete', 'fault') for c in self.cells):
            self.running = False

    def trip(self, cell, reason):
        observed=dict(temperature_c=cell['temperature_c'],voltage_v=cell['voltage_v'],
                      current_a=cell['current_a'],soh_percent=cell['soh_percent'])
        self.alarms.append(dict(cell=cell['id'],time_s=cell['time_s'],reason=reason,observed=observed))
        cell.update(status='fault',error=reason)
        self.running=False
        self.safety_stop=True
        for c in self.cells:
            c['current_a']=0
            if c['status']=='running':c['status']='stopped'
            if c['live_ml']['remaining_cycles'] is not None:
                c['live_ml']['status']='safety_stop'

    def snapshot(self):
        return dict(running=self.running, speed=self.speed, cells=self.cells,
                    temperature_min=20, temperature_max=45,alarms=self.alarms,
                    safety_stop=self.safety_stop,pending_fault=self.pending_fault)

