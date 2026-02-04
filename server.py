#!/usr/bin/env python3
import argparse, socket, ssl, threading, os, subprocess, select
from tun_iface import create_tun

BUFFER_SIZE = 2000

def setup_tun_ip(ifname, ip):
    subprocess.run(['ip', 'addr', 'del', ip, 'dev', ifname],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.check_call(['ip', 'link', 'set', ifname, 'up'])
    subprocess.check_call(['ip', 'addr', 'add', ip, 'dev', ifname])

class ClientHandler(threading.Thread):
    def __init__(self, conn, tun):
        super().__init__(daemon=True)
        self.conn = conn
        self.tun = tun

    def run(self):
        while True:
            r, _, _ = select.select([self.conn, self.tun], [], [])
            if self.conn in r:
                data = self.conn.recv(BUFFER_SIZE)
                if not data:
                    break
                os.write(self.tun, data)
            if self.tun in r:
                pkt = os.read(self.tun, BUFFER_SIZE)
                self.conn.sendall(pkt)
        self.conn.close()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cert', required=True)
    p.add_argument('--key', required=True)
    p.add_argument('--ca', required=True)
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=8443)
    p.add_argument('--tun', default='tun0')
    p.add_argument('--tun-ip', default='10.8.0.1/24')
    a = p.parse_args()

    tun = create_tun(a.tun)
    setup_tun_ip(a.tun, a.tun_ip)
    print(f"[server] {a.tun} up with {a.tun_ip}")

    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_cert_chain(a.cert, a.key)
    ctx.load_verify_locations(a.ca)

    s = socket.socket()
    s.bind((a.host, a.port))
    s.listen(5)
    print(f"[server] listening on {a.host}:{a.port}")

    while True:
        c, addr = s.accept()
        conn = ctx.wrap_socket(c, server_side=True)
        print("[server] TLS client connected")
        ClientHandler(conn, tun).start()

if __name__ == '__main__':
    main()
