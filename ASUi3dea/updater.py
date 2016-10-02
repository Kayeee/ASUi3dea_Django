from celery import Celery
#from inverterInterface import Inverter, ConnectionException
#from tasks import *

import subprocess

app = Celery('updater_worker', backend='amqp',
                      broker='amqp://Kevin:ASUi3dea@52.87.223.187/pi_env')
@app.task(name="updater.reboot_pi")
def reboot_pi():
    print "Rebooting Pi"

@app.task(name="updater.updateAuroraC")
def updateAuroraC():
    subprocess.call(["sudo", "rm", "aurora"], cwd="/usr/local/bin")
    subprocess.call(["make", "clean"], cwd="Documents/i3dea/aurora-1.9.0")
    subprocess.call(["git", "pull", "origin", "master"], cwd="Documents/i3dea/aurora-1.9.0") #need ssh key $
    subprocess.call(["sudo", "make", "install"], cwd="Documents/i3dea/aurora-1.9.0")

@app.task(name="updater.updateTasksAndInterface")
def updateTasksAndInterface():
    subprocess.call(["git", "pull", "origin", "master"], cwd="/home/pi/ASUi3dea")
    subprocess.call(["celery", "multi", "stop", "interface_worker", "-A", "tasks"], cwd="/home/pi/ASUi3dea")
    subprocess.call(["celery", "multi", "start", "interface_worker", "-A", "tasks"], cwd="/home/pi/ASUi3dea")




