#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib

from serial import Serial


def sendAT(port, bsn):
    global serial
    try:
        serial = Serial(port=port, baudrate=115200, timeout=1)
        at_bsn = bsn
        sha256 = hashlib.sha256()
        sha256.update(bsn.encode('utf-8'))
        hash = sha256.hexdigest()

        serial.write(at_bsn.encode('utf-8') + b'\r\n')
        serial.write(b'AT******\r\n')
        serial.write(b'AT******\r\n')
        serial.write(hash.encode('utf-8') + b'\r\n')
    except Exception as e:
        print(e)
    finally:
        serial.close()
