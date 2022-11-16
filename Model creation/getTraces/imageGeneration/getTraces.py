# Càrrega dels mòduls necessaris per al bon funcionament de l'eina
from urllib.parse import urlparse
from time import sleep
import selenium
from selenium import webdriver
import os
import signal
import subprocess
import pandas
import pyshark
import netifaces as ni

# Declaració de les rutes on son les carpetes que s'utilitzaràn d'input/output
cpath = "/root/"
filepath = cpath+"file/targets.csv"
dumpspath = cpath+"dumps/"
tmppath = cpath+"tmp/"
donepath = cpath+"done/"
downpath = cpath+"down/"
thirdpath = cpath+"third/"

def readCsv(file):
    input = []
    df = pandas.read_csv(file, header=None, usecols=[1], names=['Domain'])
    for entry in df['Domain']:
        input.append(entry)
    return input

def isAlreadyAnalized(elem):
    return os.path.isfile(donepath+elem+'.done') or os.path.isfile(tmppath+elem+'.onit') or os.path.isfile(downpath+elem+'.down')

def createIndicatorsOfCurrentAnalysis(elem):
    try:
        f = open(tmppath+elem+'.onit', 'x')
        f.close()
        return True
    except FileExistsError:
        return False

def executeChrome(elem):
    options = webdriver.chrome.options.Options()
    options.add_argument('--no-sandbox')

    try:
        driver = webdriver.Chrome(options=options)
    except selenium.common.exceptions.WebDriverException:
        print("[WARNING] Chrome crashed on launch. Trying again in 10 seconds...")
        sleep(10)
        driver = webdriver.Chrome(options=options)
        print("[RECOVERY] Success on re-launching Chrome")
    
    try:
        print("[INFO] Opening "+elem)
        driver.get("http://"+ elem )
        sleep(10)
        o = urlparse(driver.current_url)
        driver.close()
        if o.hostname is None:
            return False
        else:
            return o
    except selenium.common.exceptions.WebDriverException:
        websitedown = True
        print("[WARNING] "+elem+" seems to be down")
        return False

def createDown(elem):
    try:
        os.remove(dumpspath+elem+'.pcap')
        print("[WARNING] It seems "+elem+"was down. Creating "+elem+".down")
        f = open(downpath+elem+'.down', 'x')
        f.close()
        return True
    except FileExistsError:
        print("[WARNING] It seems someone created "+elem+".down faster")
        return False
            
def removeIndicatorsOfCurrentAnalysis(elem):
    print("[INFO] Removing "+elem+".onit")
    os.remove(tmppath+elem+'.onit')

def startCapture(elem):
    subprocess.Popen(['tcpdump', '-i', 'eth0', 'src', 'port', '443', 'or', 'src', 'port', '80', 'or', 'dst', 'port', '443', 'or', 'dst', 'port', '80', '-w', dumpspath + elem + '.pcap'])

def endCapture():
    try:
        tcpdump_pids = subprocess.check_output(['pidof', 'tcpdump']).split()
        for pid in tcpdump_pids:
            os.kill(int(pid), signal.SIGTERM)
    except subprocess.CalledProcessError:
        print("[WARNING] No active tcpdump found. That's strange.")

def createIndicatorsOfAnalysed(elem):
    print("[INFO] Creating "+elem+".done")
    try:
        f = open(donepath+elem+'.done', 'x')
        f.close()
        return True
    except FileExistsError:
        print("[WARNING] It seems someone created "+elem+".done faster")
        return False
    
def analyzeCapture(elem):
    for i in range(0,100):
        error = False
        while True:
            try:
                fs = pyshark.FileCapture(os.path.join(dumpspath,elem+".pcap"))
                fs.set_debug()
                if (error):
                    print("[RECOVERY] Success on opening "+elem+".pcap")
            except FileNotFoundError:
                print("[WARNING] "+elem+".pcap not found. Nonetheless, it's a typical problem. Will retry in half a sec...")
                error = True
                sleep(.5)
                continue
            break
    
    # Per a cada paquet a la captura, si l'adreça IP no és la de la nostra màquina, s'inserta a l'estructura de dades "aux"
    aux = []
    for pkt in fs:
        if 'ip' in pkt:
            if pkt.ip.src != ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']:
                aux.append(pkt.ip.src)
            elif pkt.ip.dst != ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']:
                aux.append(pkt.ip.dst)
        # La llista s'ordena alfabèticament, i es separa per espais com a un únic string
    aux = list(set(aux))
    res = ""
    first = True
    for item in aux:
        if not first:
            res = res + ' '
        res = res + item
        first = False
    return res

def dumpAnalysis(result, elem):
    print("[INFO] Creating "+elem+".third")
    try:
        f = open(thirdpath+elem+".third", 'x')
        f.write(result)
        f.close()
        return True
    except FileExistsError:
        print("[WARNING] It seems someone created "+elem+".third faster")
        return False

def removeCapture(elem):
    print("[INFO] Removing "+elem+".pcap")
    os.remove(dumpspath+elem+'.pcap')

def main():
    input = readCsv(filepath)
    for elem in input:
        if (isAlreadyAnalized(elem)):
            continue
        if (not createIndicatorsOfCurrentAnalysis(elem)):
            continue
        startCapture(elem)
        websiteUp = executeChrome(elem)
        endCapture()
        if (not createIndicatorsOfAnalysed(elem)):
            continue
        removeIndicatorsOfCurrentAnalysis(elem)
        if (websiteUp):
            result = analyzeCapture(elem)
            if (not dumpAnalysis(result, elem)):
                continue
        else:
            if (not createDown(elem)):
                continue
        removeCapture(elem)

if __name__ == "__main__":
	main()