__author__ = 'pato'

import ConnectionTestClass as vpn, time

testAgent = vpn.ConnectionTestClass()
testAgent.connect()
res = testAgent.checkConnectionState()
print res
#time.sleep(2)
testAgent.endTest()
  