__author__ = 'Patricio Cano'
import time, tempfile, pexpect, datetime, json, os

class ConnectionTestClass:
    vpnuser = ''
    vpnpass = ''
    vpnserver = ''
    vpnshort = ''
    resultDirectory = ''
    speedFileInt = ''
    speedFileExt = ''
    pingFile = ''
    lastTest = ''
    nslookupFile = ''
    prefix = ''

    def __init__(self, configFile = 'ASA.conf'):
        """
        @params: String: vpnuser, vpnpass, vpnserver

        Initialisation of parameters necessary for the Connectivity Test.
        """
        self.__readConfig(configFile)
        tmp = self.vpnserver.split('.')
        self.vpnshort = tmp[0]
        self.prefix = self.resultDirectory+self.vpnshort
        self.speedFileInt = self.prefix+'.speedInt'
        self.speedFileExt = self.prefix+'.speedExt'
        self.pingFile = self.prefix+'.ping'
        self.lastTest = self.prefix+'.lastTest'


    def beginTest(self):
        """
        @params: None

        Connect to the VPN and preform the ping and speed tests.
        4 Files are returned containing latest test, ping time, speed of connection and time to connect.
        """
        file = open(self.lastTest, 'w')
        file.write(str(datetime.datetime.now())+'\n')
        start = time.time()
        com = pexpect.spawn('openconnect -u ' + self.vpnuser + ' ' + self.vpnserver)
        com.expect('Password:')
        com.sendline(self.vpnpass)
        com.expect('Established DTLS connection')
        stop = time.time()
        tm = stop - start
        file.write('Time to connect: '+str(tm)+'\n')
        file.close()
        self.pingTest()
        self.speedTest('http://www.bbned.nl/scripts/speedtest/download/file32mb.bin', True)
        com.close()


    def speedTest(self, url, bool):
        """
        @param: String: url
        @param: boolean: bool

        Performs speed test based on url and bool. Alternate between Internal and External test.
        Returns file containing average speed of file download.
        """
        tmpfile = tempfile.mkstemp()
        com = pexpect.spawn('wget -o '+ tmpfile[1] + " "+ url, timeout=300)
        com.expect(pexpect.EOF)
        com.close()
        file = open(tmpfile[1], 'r')
        for line in file:
            if 'MB/s' in line:
                temp = line.split('(')
                tmp = temp[1].split(')')
                if bool:
                    sFile = open(self.speedFileExt, 'w')
                    sFile.write(tmp[0]+'\n')
                    sFile.close()
                else:
                    sFile = open(self.speedFileInt, 'w')
                    sFile.write(tmp[0]+'\n')
                    sFile.close()
            elif 'KB/s' in line:
                temp = line.split('(')
                tmp = temp[1].split(')')
                if bool:
                    sFile = open(self.speedFileExt, 'w')
                    sFile.write(tmp[0]+'\n')
                    sFile.close()
                else:
                    sFile = open(self.speedFileInt, 'w')
                    sFile.write(tmp[0]+'\n')
                    sFile.close()
        file.close()
        os.remove(tmpfile[1])
        os.remove(self.prefix+'file32mb.bin')

    def pingTest(self):
        """
        @params: None

        Performs ping test and retrieve ping time.
        Returns file with ping time.
        """
        com = pexpect.spawn('ping -c 1 google.de')
        com.expect('rtt')
        pingT = str(com.before).split('time=')
        ping = pingT[1].split('--')
        pFile = open(self.pingFile, 'w')
        pFile.write(ping[0])
        pFile.close()
        com.close()

    def __readConfig(self, configFile):
        tempData = open(configFile, 'r')
        data = json.load(tempData)
        self.vpnuser = data['vpnuser']
        self.vpnserver = data['vpnserver']
        self.vpnpass = data['vpnpass']
        self.resultDirectory = data['resultDirectory']

    def nsLookup(self, URL):
        com = pexpect.spawn('nslookup '+URL)
        com.expect(pexpect.EOF)
        file = open(self.nslookupFile, 'w')
        file.write(str(com.before))
        file.close()
        com.close()




