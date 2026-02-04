#!/usr/bin/env python3
# flask_gui.py — simple web UI to start/stop server & client and view logs (lab/demo)
from flask import Flask, render_template, request, jsonify
import subprocess, shlex, os, signal, time

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

procs = {'server': None, 'client': None}
logs = {'server': os.path.join(BASE_DIR, 'server.log'), 'client': os.path.join(BASE_DIR, 'client.log')}

def start_process(name, cmd):
    if procs[name] and procs[name].poll() is None:
        return f"{name} already running"
    # start and redirect stdout/stderr to log
    with open(logs[name], 'wb') as out:
        p = subprocess.Popen(shlex.split(cmd), stdout=out, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        procs[name] = p
    time.sleep(0.3)
    return f"started {name} pid={p.pid}"

def stop_process(name):
    p = procs.get(name)
    if not p or p.poll() is not None:
        return f"{name} not running"
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    except Exception:
        p.terminate()
    p.wait(timeout=3)
    return f"stopped {name}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action', methods=['POST'])
def action():
    a = request.form.get('action')
    target = request.form.get('target')
    if a == 'start':
        if target == 'server':
            cmd = f"sudo python3 {BASE_DIR}/server.py --cert {BASE_DIR}/server.crt --key {BASE_DIR}/server.key --ca {BASE_DIR}/ca.crt --host 127.0.0.1 --port 8443 --tun tun0 --tun-ip 10.8.0.1/24"
        else:
            cmd = f"sudo python3 {BASE_DIR}/client.py --cert {BASE_DIR}/client.crt --key {BASE_DIR}/client.key --ca {BASE_DIR}/ca.crt --server 127.0.0.1 --port 8443 --tun tun1 --tun-ip 10.8.0.2/24"
        result = start_process(target, cmd)
        return jsonify({'result': result})
    elif a == 'stop':
        result = stop_process(target)
        return jsonify({'result': result})
    elif a == 'log':
        # return tail of log
        logfile = logs[target]
        if not os.path.exists(logfile):
            return jsonify({'log': ''})
        with open(logfile, 'rb') as f:
            f.seek(0,2)
            size = f.tell()
            start = max(0, size-8000)
            f.seek(start)
            data = f.read().decode(errors='ignore')
        return jsonify({'log': data})
    return jsonify({'error': 'unknown'})

if __name__ == '__main__':
    # run on localhost only
    app.run(host='127.0.0.1', port=5000, debug=False)
