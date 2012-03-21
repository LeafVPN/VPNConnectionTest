#!/usr/bin/env python
__author__ = 'Patricio Cano'


import ConnectionTestClass as vpn
#vpnuser and vpnpass must be set before proceeding

testAgent = vpn.ConnectionTestClass(verbose=True)
testAgent.beginTest()
