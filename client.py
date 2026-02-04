#!/usr/bin/env python3
import argparse, socket, ssl, os, subprocess, select
from tun_iface import create_tun

BUFFER_SIZE = 2000

def setup_tun_ip(ifname, ip):
    subprocess.run(['ip', 'addr', 'del', ip, 'dev', ifname],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.check_call(['ip', 'link', 'set', ifname, 'up'])
    subprocess.check_call(['ip', 'addr', 'add', ip, 'dev', ifname])

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cert', required=True)
    p.add_argument('--key', required=True)
    p.add_argument('--ca', required=True)
    p.add_argument('--server', required=True)
    p.add_argument('--port', type=int, default=8443)
    p.add_argument('--tun', default='tun1')
    p.add_argument('--tun-ip', default='10.8.0.2/24')
    a = p.parse_args()

    tun = create_tun(a.tun)
    setup_tun_ip(a.tun, a.tun_ip)
    print(f"[client] {a.tun} up with {a.tun_ip}")

    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=a.ca)
    ctx.load_cert_chain(a.cert, a.key)

    s = socket.socket()
    s.connect((a.server, a.port))
    conn = ctx.wrap_socket(s, server_hostname=a.server)
    print("[client] connected to server over TLS")

    while True:
        r, _, _ = select.select([conn, tun], [], [])
        if conn in r:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            os.write(tun, data)
        if tun in r:
            pkt = os.read(tun, BUFFER_SIZE)
            conn.sendall(pkt)

if __name__ == '__main__':
    main()
