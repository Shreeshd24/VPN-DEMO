#!/usr/bin/env python3
# tun_iface.py — helper to create a TUN device and give the fd back

import fcntl, os, struct

# from linux/if_tun.h
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

def create_tun(name='tun0'):
    """
    Creates a TUN device with name `name` and returns its file descriptor (int).
    Requires root.
    """
    tun = os.open('/dev/net/tun', os.O_RDWR)
    ifr = struct.pack('16sH', name.encode('utf-8'), IFF_TUN | IFF_NO_PI)
    fcntl.ioctl(tun, TUNSETIFF, ifr)
    return tun
