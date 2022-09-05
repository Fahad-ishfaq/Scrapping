import time, json

from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path

outPutFileName = 'output/output.json'
url = 'https://m.cyprussportingclubs.com/'
driverPath = 'chromedriver/chromedriver.exe'

file = Path(outPutFileName)
file.touch(exist_ok=True)

# ================================================= #
# ==================  UTILS ======================= #

def loadAndWriteJson(details):
    oldDataList = []
    try:
        with open(outPutFileName, 'r') as outPutFile:
            oldDataList = json.load(outPutFile)
    except Exception as e:
        print(e)
        pass
    with open(outPutFileName, "w", encoding="utf8") as f:
        oldDataList.append(details)
        f.write(json.dumps(oldDataList, ensure_ascii=False))


# ================================================= #
# ==================  MAIN  ======================= #

def main():
    driver = webdriver.Chrome(driverPath)
    driver.maximize_window()
    driver.get(url)
    rows = driver.find_elements(By.XPATH, "//*[@class='row ng-scope']")
    for row in rows:
        details={}
        showMoreButton = row.find_elements(By.XPATH, ".//*[@ng-click='showMore(events.Id)']");
        if (showMoreButton != []):
            showMoreButton[0].click()
            points = row.text.split("\n")
            time.sleep(3)
            detailedList = {}
            for leagueDetailRows in driver.find_elements(By.XPATH, "//*[@class='container zero-margin-padding ng-scope']"):
                detailedRow = leagueDetailRows.find_element(By.XPATH, ".//div[@class='row sport_m']")
                team = detailedRow.text.replace("\n", "    ");
                detailedRow.click()
                oddsList = []
                for oddsElem in leagueDetailRows.find_elements(By.XPATH, ".//div[@ng-repeat='item in market.odds']/a"):
                    if (oddsElem.text != ""):
                        oddsList.append(oddsElem.text)
                detailedList[team] = oddsList;
            
            headerList = driver.find_elements(By.XPATH, "//*[@class='modal-header red-event-title']//div[@class='ng-binding']")
            details["league"] = headerList[0].text
            details["match"] = headerList[1].text
            details["points"] = points
            details["leagueDetails"] =detailedList
            time.sleep(2)
            driver.find_element(By.XPATH, "//*[@ui-turn-off='sportsMore']").click()
            time.sleep(2)
            loadAndWriteJson(details)
    driver.close()

if __name__ == "__main__":
    main()