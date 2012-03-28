#!/usr/bin/env python
__author__ = 'Patricio Cano'


import argparse, ConnectionTestClass as vpn
#Config File necessary.

parser = argparse.ArgumentParser(description='ASA VPN Connectivity Test:')
parser.add_argument('-v', dest='boolean_switch', action='store_true', default=False, help='Set verbose to true.')
parser.add_argument('-f', dest='config_file', action='store', default='ASA.conf', help='Set the config file, or leave blank for default.')
results = parser.parse_args()


testAgent = vpn.ConnectionTestClass(configFile=results.config_file, verbose=results.boolean_switch)
testAgent.beginTest()
