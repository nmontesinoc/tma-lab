import selenium
import pandas
from selenium import webdriver
from time import sleep

filepath = "./targets.csv"

def readCsv(file):
    input = []
    df = pandas.read_csv(file, header=None, usecols=[1], names=['Domain'])
    for entry in df['Domain']:
        input.append(entry)
    return input

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
        driver.close()
    except selenium.common.exceptions.WebDriverException:
        websitedown = True
        print("[WARNING] "+elem+" seems to be down")

def main():
    input = readCsv(filepath)
    for elem in input:
        executeChrome(elem)

if __name__ == "__main__":
	main()
