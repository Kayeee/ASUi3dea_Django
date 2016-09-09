from inverterInterface import Inverter, ConnectionException
from celery import Celery

import subprocess
import random

app = Celery('interface_worker', backend='amqp', broker='amqp://Kevin:ASUi3dea@52.87.223.187/pi_env')
app.config_from_object('celeryconfig')

@app.task(name='addTask')
def add(x, y):
    return x+y

@app.task
def initInverter(address, port):
    #for tests, address = "2" and port = "/dev/ttyUSB0"
    if address not in inverters:
        inverter = Inverter(address, port)
        inverters[address] = inverter
        return "Success"
    else:
        return "Error: Inverter is already initialized."

@app.task(name='testingfile')
def getAll(address, stringNum = "0"):
    inverter = Inverter()
    result = inverter.getAll("0")
    return result
    # try:
    #     result = JSONify(inverters[address].getAll(stringNum))
    #     return result
    # except ConnectionException:
    #     return "Error: Cannot connect to inverter."
    # except KeyError:
    #     return "Error: Address not found."

@app.task(name='getAlle')
def getAlle(address, stringNum = "0"):
    inverter = Inverter()
    result = inverter.getAlle("0")
    return result

@app.task
def updateAuroraC():
    try:
        subprocess.call(["sudo", "rm", "aurora"], cwd="/usr/local/bin")
    except OSError:

        print "aurora not found"

    subprocess.call(["make", "clean"], cwd="Documents/i3dea/aurora-1.9.0")
    subprocess.call(["git", "pull", "origin", "master"], cwd="Documents/i3dea/aurora-1.9.0") #need ssh key for this
    subprocess.call(["sudo", "make", "install"], cwd="Documents/i3dea/aurora-1.9.0")
    return "Complete"


@app.task
def updateAuroraC_e():
    try:
        subprocess.call(["sudo", "rm", "aurorae"], cwd="/usr/local/bin")
    except OSError:
        print "aurora not found"
    subprocess.call(["make", "clean"], cwd="Documents/i3dea/aurora-exp")
    subprocess.call(["git", "pull", "origin", "aurora_exp"], cwd="Documents/i3dea/aurora-exp") #need ssh key for this
    subprocess.call(["sudo", "make", "install"], cwd="Documents/i3dea/aurora-exp")
    return "Complete"

def JSONify(data):
    return "{" + data + "}"

@app.task
def createData():
    input_voltage = "\"inputvoltage\": {:.5f},".format(random.uniform(220.0, 260.0))
    input_current = "\"inputcurrent\": {:.5f},".format(random.uniform(4.0, 7.0))
    input_power = "\"inputpower\": {:.5f},".format(random.uniform(1300.0, 1500.0))
    grid_voltage = "\"gridvoltage\": {:.5f},".format(random.uniform(220.0, 260.0))
    grid_current = "\"gridcurrent\": {:.5f},".format(random.uniform(4.0, 7.0))
    grid_power = "\"gridpower\": {:.5f},".format(random.uniform(1300.0, 1500.0))
    frequency = "\"frequency\": {:.5f},".format(random.uniform(50.0, 70.0))
    conversion_efficiency = "\"conversionefficiency\": {:.1f},".format(random.uniform(80.0, 99.0))
    inverter_temperature = "\"invertertemperature\": {:.5f},".format(random.uniform(80.0, 99.0))
    daily_energy = "\"dailyenergy\": {:.5f},".format(random.uniform(0.1, 50.0))
    weekly_energy = "\"weeklyenergy\": {:.5f},".format(random.uniform(0.1, 120.0))
    monthly_energy = "\"monthlyenergy\": {:.5f},".format(random.uniform(0.1, 600.0))
    yearly_energy = "\"yearlyenergy\": {:.5f},".format(random.uniform(0.1, 4000.0))
    total_energy = "\"totalenergy\": {:.5f}".format(random.uniform(15000.1, 16000.0))

    return """
    {{
        \"inverter\": "0",
        {0}
        {1}
        {2}
        {3}
        {4}
        {5}
        {6}
        {7}
        {8}
        \"cumulatedenergy\": {{
            {9}
            {10}
            {11}
            {12}
            {13}
        }}
    }}
    """.format(input_voltage, input_current, input_power, grid_voltage, grid_current, grid_power, frequency, conversion_efficiency, inverter_temperature, daily_energy, weekly_energy, monthly_energy, yearly_energy, total_energy)
