import requests, csv, os
from bs4 import BeautifulSoup

NUMBER=1
BASE_PATH = os.getcwd() #+ "/Scrapping/ExpresShighs"
FILE_NAME = f"/resources/in{NUMBER}.csv"
OUTPUT_FILE_NAME=f"/resources/out{NUMBER}.csv"
EX_FILE_NAME=f"/resources/ex{NUMBER}.csv"
file = open (BASE_PATH + FILE_NAME)
file_reader = csv.reader(file)


def writeFile(file_name, line):
    with open(file_name, "a", encoding="UTF8", newline="") as f:
        f.write("\n" + line)
        f.close()

def getKnownResponses(status):
    match status:
        case 200:
            return "Page loads normally"
        case 404:
            return "Page not found"
        case _:
            return None

i=1
for row in file_reader:
    print(i)
    i+=1
    response = requests.get(row[0])
    soup = BeautifulSoup(response.text.replace("\n", ""), "html.parser")
    content = soup.find("div", {"id":"content"})
    if (content != None):
        content = str (content)
        content = content.replace("\n", "").replace("\t", "").replace("\"", "'")
    knownResponse = getKnownResponses(response.status_code)
    if (knownResponse == None):
        writeFile(BASE_PATH + EX_FILE_NAME, f"\"{row[0]}\", \"{response.status_code}\", \"{knownResponse}\"")

    writeFile(BASE_PATH + OUTPUT_FILE_NAME, f"\"{row[0]}\", \"{response.status_code}\", \"{knownResponse}\", \"{content}\"")
        
file.close()
