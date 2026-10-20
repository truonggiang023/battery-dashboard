"""One shared legacy simulation rack; controls never operate physical equipment."""
import threading, time, copy
from integrations.digital_twin.rack import Rack

_rack=None
_guard=threading.Lock()

def rack():
    global _rack
    with _guard:
        if _rack is None:
            _rack=Rack()
            threading.Thread(target=_worker,args=(_rack,),daemon=True).start()
        return _rack

def _worker(model):
    previous=time.monotonic()
    while True:
        time.sleep(.1);now=time.monotonic()
        with model.lock:model.tick(now-previous)
        previous=now

def state():
    model=rack()
    with model.lock:return copy.deepcopy(model.snapshot())

def control(body):
    if not isinstance(body,dict):raise ValueError('Nội dung điều khiển không hợp lệ.')
    action=body.get('action');model=rack()
    if action not in ('start','pause','reset','speed'):raise ValueError('Chỉ hỗ trợ start, pause, reset, speed trong dashboard này.')
    with model.lock:
        if action=='start' and model.safety_stop:raise ValueError('Rack đang STOP; cần Reset trước khi chạy lại.')
        if action=='reset':model.reset()
        elif action=='speed':
            if type(body.get('speed')) is not int or body['speed'] not in (1,10,60,300):raise ValueError('Speed phải là 1, 10, 60 hoặc 300.')
            model.speed=body['speed']
        else:model.running=action=='start'
        return copy.deepcopy(model.snapshot())
