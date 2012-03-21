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
    internalURL = ''
    externalURL = ''
    group = ''
    verbose = False

    def __init__(self, configFile = 'ASA.conf', verbose = False):
        """
        @params: configFile

        Initialisation of parameters necessary for the Connectivity Test.
        """
        self.verbose = verbose
        self.__readConfig(configFile)
        tmp = self.vpnserver.split('.')
        self.vpnshort = tmp[0]
        self.prefix = self.resultDirectory+self.vpnshort
        self.speedFileInt = self.prefix+'.speedInt'
        self.speedFileExt = self.prefix+'.speedExt'
        self.pingFile = self.prefix+'.ping'
        self.nslookupFile = self.prefix+'.DNS'
        self.lastTest = self.prefix+'.lastTest'


    def beginTest(self):
        """
        @params: None

        Connect to the VPN and preform the ping and speed tests.
        4 Files are returned containing latest test, ping time, speed of connection and time to connect.
        """
        self.__printLog('Beginning Test...')
        try:
            file = open(self.lastTest, 'w')
            file.write(str(datetime.datetime.now())+'\n')
            start = time.time()
            self.__printLog('Attempting to connect...')
            com = pexpect.spawn('openconnect -u ' + self.vpnuser + ' ' + self.vpnserver)
            if 'asa3' in self.vpnserver:
                com.expect('GROUP:')
                com.sendline(self.group)
            com.expect('Password:')
            com.sendline(self.vpnpass)
            com.expect('Established DTLS connection')
            stop = time.time()
            tm = stop - start
            self.__printLog('Connection established.')
            file.write('Time to connect: '+str(tm)+'\n')
            file.close()
            com.close()
        except Exception as exc:
            print(exc)
            print('Could not connect to ASA server')
            exit(1)
        self.__pingTest()
        self.__nsLookup('uni-stuttgart.de')
        self.__speedTest(self.externalURL, True)
        self.__printLog('Test completed successfully!')
        #self.__speedTest(self.externalURL, False)



    def __speedTest(self, url, isExternal):
        """
        @param: url
        @param: isExternal

        Performs speed test based on url and isExternal. Alternate between Internal and External test.
        Returns file containing average speed of file download.
        """
        self.__printLog('Speed Test Started...')
        try:
            tmpfile = tempfile.mkstemp()
            self.__printLog('Fetching remote file...')
            com = pexpect.spawn('wget -o '+ tmpfile[1] + " "+ url, timeout=300)
            com.expect(pexpect.EOF)
            com.close()
            self.__printLog('File downloaded successfully.')
            file = open(tmpfile[1], 'r')
            for line in file:
                if 'MB/s' in line:
                    temp = line.split('(')
                    tmp = temp[1].split(')')
                    if isExternal:
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
                    if isExternal:
                        sFile = open(self.speedFileExt, 'w')
                        sFile.write(tmp[0]+'\n')
                        sFile.close()
                    else:
                        sFile = open(self.speedFileInt, 'w')
                        sFile.write(tmp[0]+'\n')
                        sFile.close()
            file.close()
            os.remove(tmpfile[1])
            os.remove(self.resultDirectory+'file32mb.bin')
        except Exception:
            print('Speed Test Failed: Address Host unreachable.')
            exit(1)

    def __pingTest(self):
        """
        @params: None

        Performs ping test and retrieve ping time.
        Returns file with ping time.
        """
        self.__printLog('Ping Test Started...')
        try:
            com = pexpect.spawn('ping -c 1 google.de')
            com.expect('rtt')
            pingT = str(com.before).split('time=')
            ping = pingT[1].split('ms')
            pFile = open(self.pingFile, 'w')
            pFile.write(ping[0])
            pFile.close()
            com.close()
            self.__printLog('Ping Test successful.')
        except Exception:
            print('An error occurred during the ping operation')
            pFile = open(self.pingFile, 'w')
            pFile.write('Ping failed')
            pFile.close()

    def __nsLookup(self, URL):
        """
        @params URL

        Preforms a DNS Lookup against the give URL.
        """
        self.__printLog('DNS lookup Started...')
        try:
            com = pexpect.spawn('nslookup '+URL)
            com.expect(pexpect.EOF)
            file = open(self.nslookupFile, 'w')
            file.write(str(com.before))
            file.close()
            com.close()
            self.__printLog('DNS lookup successful.')
        except Exception:
            print('DNS Lookup Failed.')
            file = open(self.nslookupFile, 'w')
            file.write('Last DNS Lookup failed.')
            file.close()


    def __readConfig(self, configFile):
        """
        @params configFile

        Reads a config file containing different parameters and loads them into the appropriate local parameters.
        """
        self.__printLog('Reading config file...')
        try:
            tempData = open(configFile, 'r')
            data = json.load(tempData)
            self.vpnuser = data['vpnuser']
            self.vpnserver = data['vpnserver']
            self.vpnpass = data['vpnpass']
            self.resultDirectory = data['resultDirectory']
            self.internalURL = data['internalURL']
            self.externalURL = data['externalURL']
            self.group = data['group']
            self.__printLog('Config file successfully loaded.')
        except Exception:
            print('Config file could not be loaded!')
            print('File not present or badly formatted JSON.')
            exit(1)

    def __printLog(self, out):
        """
        @params out

        Prints a LOG output if the verbose flag is raised.
        """
        if self.verbose:
            print(out)
        else:
            pass
