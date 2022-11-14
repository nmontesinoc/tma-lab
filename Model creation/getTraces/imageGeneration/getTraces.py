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

# Declaració de l'estructura de dades on hi seràn totes les pàgines web a partir del fitxer CSV
input = []

# Bolcat de totes les pàgines del CSV a l'estructura de dades
df = pandas.read_csv(filepath, header=None, usecols=[1], names=['Domain'])
for entry in df['Domain']:
    input.append(entry)

# Per a poder còrrer Chrome com a root, s'ha de posar aquesta opció
options = webdriver.chrome.options.Options()
options.add_argument('--no-sandbox')

# Per a cada pàgina web de la llista
for elem in input:
    # A aquest punt suposem que la pàgina no està caiguda
    websitedown = False

    # Si hi ha cap contenidor que estigui analitzant o que ja hagi analitzat la pàgina en qüestió, es passa a la següent de la llista
    if os.path.isfile(donepath+elem+'.done') or os.path.isfile(tmppath+elem+'.onit') or os.path.isfile(downpath+elem+'.down'):
        continue
    # En cas que es vagi a analitzar la pàgina, es crea l'arxiu .onit
    else:
        print("[INFO] "+elem+".onit, "+elem+".done and "+elem+".down not found. Creating "+elem+".onit")
        try:
            f = open(tmppath+elem+'.onit', 'x')
            f.close()
        # En aquest punt, és possible que hi hagi algun problema de race condition. D'aquesta manera, s'evita i es passa a la següent pàgina de la llista
        except FileExistsError:
            print("[WARNING] It seems someone created "+elem+".onit faster")
            continue
    # S'executa Chrome. Si per saturació del sistema no s'ha pogut executar, es torna a intentar en deu segons
    try:
        driver = webdriver.Chrome(options=options)
    except selenium.common.exceptions.WebDriverException as e:
        print("[WARNING] Chrome crashed on launch. Trying again in 10 seconds...")
        sleep(10)
        driver = webdriver.Chrome(options=options)
        print("[RECOVERY] Success on re-launching Chrome")
    # S'executa Tcpdump, capturant tot el tràfic que vagi o provingui dels ports 80 i 443
    tcpdump = subprocess.Popen(['tcpdump', '-i', 'eth0', 'src', 'port', '443', 'or', 'src', 'port', '80', 'or', 'dst', 'port', '443', 'or', 'dst', 'port', '80', '-w', dumpspath + elem + '.pcap'])
    # S'obre la pàgina a Chrome, s'espera deu segons i es tanca
    try:
        print("[INFO] Opening "+elem)
        driver.get("http://"+ elem )
        sleep(10)
        o = urlparse(driver.current_url)
        driver.close()
        # Es tanca Tcpdump. De vegades no es troba un Tcpdump actiu per alguna raó que es desconeix (probablement race condition, cosa la qual no ens afecta a aquest punt)
        try:
            tcpdump_pids = subprocess.check_output(['pidof', 'tcpdump']).split()
            for pid in tcpdump_pids:
                os.kill(int(pid), signal.SIGTERM)
        except subprocess.CalledProcessError:
            print("[WARNING] No active tcpdump found. That's strange.")
        # Es crea l'arxiu .done. En aquest punt, és possible que hi hagi algun problema de race condition, que ja es controla passant a la seguent pàgina
        print("[INFO] Creating "+elem+".done")
        try:
            f = open(donepath+elem+'.done', 'x')
            f.close()
        except FileExistsError:
            print("[WARNING] It seems someone created "+elem+".done faster")
            continue
    # En cas que Selenium retorni aquesta excepció, vol dir que no s'ha pogut accedir a la pàgina. Es declara aquesta execució com a caiguda
    except selenium.common.exceptions.WebDriverException:
        websitedown = True
        print("[WARNING] "+elem+" seems to be down")
        # Es tanca Tcpdump. De vegades no es troba un Tcpdump actiu per alguna raó que es desconeix (probablement race condition, cosa la qual no ens afecta a aquest punt)
        try:
            tcpdump_pids = subprocess.check_output(['pidof', 'tcpdump']).split()
            for pid in tcpdump_pids:
                os.kill(int(pid), signal.SIGTERM)
        except subprocess.CalledProcessError:
            print("[WARNING] No active tcpdump found. That's strange.")
        # S'esborra la captura de Tcpdump i es crea l'arxiu .down. Es controlen les possibles race conditions.
        print("[WARNING] Removing "+elem+".pcap because the website is down")
        os.remove(dumpspath+elem+'.pcap')
        print("[WARNING] Creating "+elem+".down because the website is down")
        try:
            f = open(downpath+elem+'.down', 'x')
            f.close()
        except FileExistsError:
            print("[WARNING] It seems someone created "+elem+".down faster")
            continue
    # Es borra l'arxiu .onit
    print("[INFO] Removing "+elem+".onit")
    os.remove(tmppath+elem+'.onit')
    # S'ha detectat que Selenium ens indica que la pàgina està caiguda per exepció o bé per la variable o.hostname. Es controla
    if not websitedown:
        # En cas que la web estigui caiguda (detectat per o.hostname), es crea .down i s'esborra l'arxiu .pcap. Es controlen les possibles race conditions.
        if o.hostname is None:
            print("[WARNING] It seems "+elem+"was down. Creating "+elem+".down")
            try:
                f = open(downpath+elem+'.down', 'x')
                f.close()
            except FileExistsError:
                print("[WARNING] It seems someone created "+elem+".down faster")
                continue
            print("[WARNING] It seems "+elem+" was down. Removing "+elem+".pcap")
            os.remove(dumpspath+elem+'.pcap')
            continue
        # S'obre Pyshark per a poder fer l'anàlisi de la captura. En cas que no es pogui, s'intenta obrir un altre cop (de vegades passa que l'arxiu .pcap encara no hi és disponible)
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
        # Es crea l'arxiu .third i es bolca el contingut de l'string anteriorment creat. Es controla la possible race condition.
        print("[INFO] Creating "+elem+".third")
        try:
            f = open(thirdpath+elem+".third", 'x')
            f.write(res)
            f.close()
        except FileExistsError:
            print("[WARNING] It seems someone created "+elem+".third faster")
            continue