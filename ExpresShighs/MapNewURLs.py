from bs4 import BeautifulSoup
import os
BASE_PATH=os.getcwd()
XML_FILE_NAME=BASE_PATH + "/resources/test.xml"
data=None
with open(XML_FILE_NAME, 'r') as f:
    data = f.read()

data_bs = BeautifulSoup(data, "xml")
urls = data_bs.find_all("url")
for url in urls:
    print(url.find("loc").text)