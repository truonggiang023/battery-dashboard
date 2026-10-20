"""Single-process WSGI entry point (shared simulation rack and workbook locks)."""
import argparse, os
from waitress import serve

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',default='127.0.0.1')
    parser.add_argument('--port',type=int,default=5000)
    parser.add_argument('--local',action='store_true',help='Allow local development without login')
    args=parser.parse_args()
    if not args.local and not (os.environ.get('DASHBOARD_USERNAME') and os.environ.get('DASHBOARD_PASSWORD')):
        parser.error('Set DASHBOARD_USERNAME and DASHBOARD_PASSWORD before shared use; --local is for local development only.')
    if args.local and args.host not in ('127.0.0.1','localhost'):
        parser.error('--local requires a loopback host. For shared hosting, configure credentials and HTTPS.')
    from app import app
    serve(app,host=args.host,port=args.port,threads=8)
