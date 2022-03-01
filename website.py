import time, sys, socket, argparse, os.path, json, threading, glob
import importlib
import netifaces
import pytz_deprecation_shim as pds

from utils.functions import Functions
from os import listdir
from utils.singleton import Singleton

from netifaces import interfaces, ifaddresses, AF_INET



## Parameter reader (from file) and args
def checkParameter(args):
    singleton=Singleton()
    # If debug
    if args.debug:
        Functions.log("INF","Debug activated","CORE")
        singleton.debug=True

    # Populate version
    singleton.version="not_set"

    # Read configuration file json
    configFile=os.path.abspath(args.configFile)
    if not os.path.isfile(configFile):
        Functions.log("DEAD","File " + str(configFile) + " doesn't exist","CORE")
    Functions.log("INF","Config file exist " + configFile,"CORE")
    singleton.configFile=configFile

    # Setting current hostname & ip
    singleton.hostName=socket.gethostname()
    for ifaceName in interfaces():
          addrs=ifaddresses(ifaceName)
          try:
              for subAdress in addrs[netifaces.AF_INET]:
                  if subAdress["addr"] != "127.0.0.1":
                      Functions.log("INF","Local ip detected " + str(subAdress["addr"]),"CORE")
                      singleton.ip=str(subAdress["addr"])
          except Exception as err:
              Functions.log("WNG","Error while trying to detect local ip " + str(err),"CORE")
              pass

    # Parsing the configFile
    Functions.log("DBG","Parsing configFile " + configFile,"CORE")
    try:
        jsonLine=Functions.loadFileInALine(configFile)
        singleton.parameters=json.loads(jsonLine)
        singleton.debug=singleton.parameters["debug"]
        Functions.log("DBG","Json config file successfully loaded " +  json.dumps(singleton.parameters,indent=4),"CORE")
    except Exception as err:
        Functions.log("DEAD","Can't parse file " + configFile + " is it a json file ? details " + str(err),"CORE")

  

def startDaemons():
    Functions.log("DBG","Start daemons now","CORE")
    singleton=Singleton()
    try:
        Functions.log("DBG","Add backgroundJob to scheduler with " + str(singleton.parameters["backgroundJobInterval"]) + " sec(s) interval","CORE")
        singleton.internalScheduler.add_job(backgroundJob, 'interval', seconds=singleton.parameters["backgroundJobInterval"])
    except Exception as err:
        Functions.log("ERR","Error with scheduler " + str(err),"CORE")

def backgroundJob():
    Functions.log("DBG","Start background job","CORE")
    singleton=Singleton()
    Functions.log("DBG","End background job","CORE")
    


def startWeb():
    singleton=Singleton()
    # Ok now check if we webserver is asked
    if singleton.parameters["webserver"] :
        Functions.log("DBG","Webserver is asked, starting it","CORE")
        importlib.import_module('web')
        Functions.log("DBG","Trying instanciation of " + str(singleton.parameters["webClass"]),"CORE")
        mod=importlib.import_module('.' + singleton.parameters["webClass"],package="web")
        aSiteClass = getattr(mod, singleton.parameters["webClass"])
        singleton.instanceWebApp=aSiteClass()
    else:
        Functions.log("DBG","Webserver not asked","CORE")


def waitEnd():
    while True:
         Functions.log("DBG","PimpMyPhototheque still alive","CORE")
         time.sleep(2)


## start
def pimpMyPhototheque():
    pds.helpers.upgrade_tzinfo("Europe/Paris")
    Functions.log("INF","Instanciate Singleton","CORE")
    singleton=Singleton()
    Functions.log("INF","Starting pimpMyPhototheque on " + socket.gethostname(),"CORE")
    Functions.log("INF","Analysing arguments","CORE")
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile",help="The absolute path to the configuration file (pimpMyPhototheque.json)")
    parser.add_argument("--debug",help="Debug mode, more verbosity",action="store_true")
    args = parser.parse_args()
    
    checkParameter(args)

    # Web starting
    waitServer=threading.Thread(target=startWeb)
    waitServer.start()

   
    waitThread=threading.Thread(target=waitEnd)
    waitThread.start()

    startDaemons()
    waitServer.join()

if __name__ == '__main__':
    pimpMyPhototheque()