import subprocess

#subprocess.call(["ls", "-l"])
class ConnectionException(Exception):
    pass

class Inverter:
    address = "2"
    serialPort = "/dev/ttyUSB0"

    def getCumulatedEnergies(self):
        result = subprocess.Popen(["aurora", "-a", self.address, "-e", "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getDSP(self, stringNum = "0"):
        result = subprocess.Popen(["aurora", "-a", self.address, "-d", stringNum, "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getPartNum(self):
        result = subprocess.Popen(["aurora", "-a", self.address, "-p", "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getSerialNum(self):
        result = subprocess.Popen(["aurora", "-a", self.address, "-n", "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getFirmWare(self):
        result = subprocess.Popen(["aurora", "-a", self.address, "-f", "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getManufacturingDate(self):
        result = subprocess.Popen(["aurora", "-a", self.address, "-m", "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getVersion(self):
        result = subprocess.Popen(["aurora", "-a", self.address, "-v", "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getAll(self, stringNum = "0"):
        result = subprocess.Popen(["aurora", "-a", self.address, "-e", "-d", stringNum, "-p", "-n", "-f", "-m", "-v", "-J", self.serialPort, "-Y", "10"], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getData(self, stringNum = "0"):
        result = subprocess.Popen(["aurora", "-a", self.address, "-e", "-d", stringNum, "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def getInfo(self):
        result = subprocess.Popen(["aurora", "-a", self.address,  "-p", "-n", "-f", "-m", "-v", "-J", self.serialPort], stdout=subprocess.PIPE)
        out, err = result.communicate()
        return out

    def checkException(self, result):
        if "ERROR:" in result:
            raise ConnectionException("Error: Cannot connect to inverter.")

    def runErrorCheck(self):
        raise ConnectionException("Error: Testing")
