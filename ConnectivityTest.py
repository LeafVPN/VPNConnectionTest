#!/usr/bin/env python
__author__ = 'Patricio Cano'


import argparse, ConnectionTestClass as vpn
#Config File necessary.

testAgent = vpn.ConnectionTestClass(verbose=True)
testAgent.beginTest()
