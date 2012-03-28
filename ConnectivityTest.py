#!/usr/bin/env python
__author__ = 'Patricio Cano'


import argparse, ConnectionTestClass as vpn
#Config File necessary.

parser = argparse.ArgumentParser(description='ASA VPN Connectivity Test:')
parser.add_argument('-v', dest='boolean_switch', action='store_true', default=False, help='Set verbose to true.')
results = parser.parse_args()


testAgent = vpn.ConnectionTestClass(verbose=results.boolean_switch)
testAgent.beginTest()
