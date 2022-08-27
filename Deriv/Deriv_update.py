from selenium import webdriver
import time
import csv, re

import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui, itertools
import playsound
import requests



a_file = open("login_info_updated.txt", "r")
list_of_lines = a_file.readlines()

mail = list_of_lines[0]
password = list_of_lines[1]
sellingrate = float(list_of_lines[2])
ProfitLKR = int(list_of_lines[3]) # rate
ProfitPercentage = float(list_of_lines[4]) # usd limit

BankBalance = int(list_of_lines[5]) # BankBalance
BankCharges = int(list_of_lines[6])
RefreshTime =  int(list_of_lines[7])


print("mail = ",mail)

print("sellingrate = ",sellingrate)
print("ProfitLKR = ",ProfitLKR)
print("ProfitPercentage = ",ProfitPercentage)

print("BankBalance = ",BankBalance)
print("BankCharges = ",BankCharges)
print("RefreshTime = ",RefreshTime)




pyautogui.alert(text="Please Check if these conditions are correct? ", title='Confirmation', button='OK')

try:
    url = "https://app.deriv.com/"
    driver = webdriver.Chrome("chromedriver.exe")
    driver.set_window_size(1280,800)
    driver.get(url)

    cls = lambda: os.system('cls')
except:
    try:
        requests.get('https://app.deriv.com/').status_code
        print("Connected")
    except:
        print("Not Connected")
        playsound.playsound("alert5.wav")
        time.sleep(3)
        exit()
        




    




def login():
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID , "dt_login_button"))).click()
        driver.find_element_by_id("txtEmail").send_keys(Keys.CONTROL, 'a')
        time.sleep(1)
        
        driver.find_element_by_id("txtEmail").send_keys(mail)
        time.sleep(3)
        driver.find_element_by_id("txtPass").send_keys(Keys.BACKSPACE)
        time.sleep(2)
        driver.find_element_by_id("txtPass").send_keys(password)
        time.sleep(3)
        print('mail',mail)
        print('password',password)
        # driver.find_element_by_name("login").click()
        
    except:
        try:
            login()
        except:
            print("login pass")
            pass



def buy():
    try:                                                                        
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[1]/ul/div/li[1]"))).click()
        
        time.sleep(5)
    except:
        try:
            time.sleep(3)
            
            driver.get("https://app.deriv.com/")
            time.sleep(3)

                                                                                    
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dt_cashier_tab']/span"))).click()
            #driver.get("https://app.deriv.com/cashier/p2p")
            time.sleep(5)
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dc_dp2-p_link']"))).click()
            time.sleep(5)

            
        except:
            print('Condition 1')
            pass

    try:
        last_scroll_height = 1
        print("         Checking New Orders")
        print("-------------------------------------")
        while True:
            rate3 = driver.find_elements_by_xpath("//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div[3]/span")        
            
            key = 1
            for i in rate3:    
                
                a_file = open("login_info_updated.txt", "r")
                list_of_lines = a_file.readlines()
                BankBalance = int(list_of_lines[5]) # BankBalance
                #print("BankBalance",BankBalance)
                rate = i.text
                
                num2 = list(re.split(" ", rate))
                USDRate = float(num2[0])
                #print(USDRate)
                if USDRate < sellingrate: #condition 1
                
                    string = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[2]".format(key)               
                    maxUSD = driver.find_element_by_xpath(string).text    
                        
                    maxUSD2 = list(re.split(" |–", maxUSD))      
                    minUSD =  float(maxUSD2[0])        
                    print("minUSD:",minUSD)
                    MaxUSDAvailable = float(maxUSD2[1])
                    # print("MaxUSDAvailable",MaxUSDAvailable)
                    
                    # print("USDRate*MaxUSDAvailable)+BankCharges",(USDRate*MaxUSDAvailable)+BankCharges)
                    if BankBalance >= ((USDRate*MaxUSDAvailable)+BankCharges):
                        calculatedProfit = (((sellingrate*MaxUSDAvailable)-(USDRate*MaxUSDAvailable))-BankCharges)
                        
                        #print("calculatedProfit",calculatedProfit)
                        if calculatedProfit >= ProfitLKR:
                            CalculatedPercentage = (((calculatedProfit)/((USDRate*MaxUSDAvailable)+BankCharges))*100)
                            # print("ProfitLKR        :",ProfitLKR)
                            # print("calculatedProfit : ",calculatedProfit)
                            # print("CalculatedPercentage",CalculatedPercentage)
                            
                            if CalculatedPercentage >= ProfitPercentage:
                                
                                
                                
                                string2 = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[1]/div/div[2]/div".format(key)
                                BuyButt = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[4]/button".format(key)
                                
                                name = driver.find_element_by_xpath(string2).text
                                
                                if name == "Invita":
                                    print("name:Invita:::", name)
                                    pass
                                
                                else:
                                    print('This name have your offer condition true:   ',name)
                                    print('Condition 1: Profit in LKR = ',calculatedProfit)
                                    print('Condition 2: Profit% = ',CalculatedPercentage)
                                    
                                    driver.find_element_by_xpath(BuyButt).click()
                                    time.sleep(1)
                                    driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(Keys.CONTROL, 'a')
                                    time.sleep(1)
                                    driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(Keys.BACKSPACE)
                                    time.sleep(1)
                                    driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(int(MaxUSDAvailable))
                                    time.sleep(1)

                                    
                                    
                                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='modal_root']/div/div/div[3]/div/button[2]"))).click()
                                    for i in range(5):    
                                        playsound.playsound("alert.wav")
                                    
                                    # CheckStatus = OrderConfirmStatus()
                                    #     # if CheckStatus == True:
                                    # print("CheckStatus1",CheckStatus)
                                    
                                    print("\n")
                                    BankBalance_new = BankBalance - (USDRate*MaxUSDAvailable)
                                    print('Remaning Balance : ',BankBalance_new)
                                    a_file = open("login_info_updated.txt", "r")
                                    list_of_lines = a_file.readlines()
                                    list_of_lines[5] =  "{}\n".format(int(BankBalance_new))
                                    
                                    a_file = open("login_info_updated.txt", "w")
                                    a_file.writelines(list_of_lines)
                                    a_file.close()
                                    
                                    time.sleep(5)
                                    driver.get("https://app.deriv.com/cashier/p2p")
                                    time.sleep(3)
                                    buy()
                            
                            else:
                                print(("Calculated percentage {} % is less than given {} % ").format(int(CalculatedPercentage) , ProfitPercentage))
                        else:
                            print(("Calculated Profit {}  is less than given Profit {}  ").format(calculatedProfit , ProfitLKR))




                    elif BankBalance < ((USDRate*MaxUSDAvailable)+BankCharges):
                        print("Bank Balance is less than required so making adjustments")
                        MaxUSDAvailable = int((BankBalance-BankCharges)/USDRate)
                       #MaxUSDAvailable = int(MaxUSDAvailable)
                        print("Amount I am going to Buy: ",MaxUSDAvailable)
                        calculatedProfit = (((sellingrate*MaxUSDAvailable)-(USDRate*MaxUSDAvailable))-BankCharges)
                        # print("calculatedProfit",calculatedProfit)
                        if MaxUSDAvailable < minUSD:
                            print("Bank Balance is lower than minimun Limit :",minUSD)
                            time.sleep(3)
                            pass
                        
                        else:
                            if calculatedProfit >= ProfitLKR:
                                #print("calculatedProfit",calculatedProfit)
                                # print("ProfitLKR",ProfitLKR)
                                # print("(calculatedProfit)/((sellingrate - USDRate)+BankCharges)",((calculatedProfit)/(((sellingrate-USDRate)*MaxUSDAvailable)+BankCharges))*100)
                                # print("ProfitPercentage",ProfitPercentage)
                                CalculatedPercentage = (((calculatedProfit)/((USDRate*MaxUSDAvailable)+BankCharges))*100)
                                
                                if CalculatedPercentage >= ProfitPercentage:
                                    string2 = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[1]/div/div[2]/div".format(key)
                                    BuyButt = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[4]/button".format(key)
                                    
                                    name = driver.find_element_by_xpath(string2).text
                                
                                    if name == "Invita":
                                        print("name:Invita:::", name)
                                        pass
                                    
                                    else:
                                        print("Buying after reducing limit")
                                        print('These name have your offer condition true:   ',name)
                                        print('Condition 1: Profit in LKR = ',calculatedProfit)
                                        print('Condition 2: Profit% = ',CalculatedPercentage)
                                        
                                        driver.find_element_by_xpath(BuyButt).click()
                                        time.sleep(1)
                                        driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(Keys.CONTROL, 'a')
                                        time.sleep(1)
                                        driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(Keys.BACKSPACE)
                                        time.sleep(1)
                                        driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(int(MaxUSDAvailable))
                                        time.sleep(1)
                                        
                                        
                                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='modal_root']/div/div/div[3]/div/button[2]"))).click()
                                        
                                        for i in range(5):    
                                            playsound.playsound("alert.wav")

                                        # CheckStatus = OrderConfirmStatus()
                                        # # if CheckStatus == True:
                                        # print("CheckStatus",CheckStatus)
                                        
                                        print("\n")
                                        BankBalance_new = BankBalance - (USDRate*MaxUSDAvailable)
                                        print('Remaning Balance : ',BankBalance_new)
                                        a_file = open("login_info_updated.txt", "r")
                                        list_of_lines = a_file.readlines()
                                        list_of_lines[5] =  "{}\n".format(int(BankBalance_new))
                                        
                                        a_file = open("login_info_updated.txt", "w")
                                        a_file.writelines(list_of_lines)
                                        a_file.close()
                                        
                                        time.sleep(5)
                                        driver.get("https://app.deriv.com/cashier/p2p")
                                        time.sleep(3)
                                        buy()
                                        
                                        # else:
                                        #     print("Order is not placed so bank Amount is not deducted.")

                                else:
                                    print(("2 Calculated percentage {} % is less than given {} % ").format(int(CalculatedPercentage) , ProfitPercentage))
                            else:
                    
                                print(("2 Calculated Profit {}  is less than given Profit {}  ").format(calculatedProfit , ProfitLKR))

                else:
                    print(("USD Rate  {} is  greater than Selling Price {}  ").format(USDRate , sellingrate))
                key += 1
                
            driver.execute_script("document.querySelector('#app_contents > div > div > div > div > div.dc-page-overlay__content > div > div.dc-vertical-tab__content.dc-vertical-tab__content--floating > div > main > div > div.dc-tabs__content.dc-tabs__content--p2p-cashier__tabs > div > div.dc-table.buy-sell__table > div.buy-sell__table-body > div > div > div > div:nth-child(1) > div > div').scrollTo(0, document.querySelector('#app_contents > div > div > div > div > div.dc-page-overlay__content > div > div.dc-vertical-tab__content.dc-vertical-tab__content--floating > div > main > div > div.dc-tabs__content.dc-tabs__content--p2p-cashier__tabs > div > div.dc-table.buy-sell__table > div.buy-sell__table-body > div > div > div > div:nth-child(1) > div > div').scrollHeight);")
            # ##driver.execute_script("window.scrollTo(0, document.querySelector('#app_contents > div > div > div > div > div.dc-page-overlay__content > div > div.dc-vertical-tab__content.dc-vertical-tab__content--floating > div > main > div > div.dc-tabs__content.dc-tabs__content--p2p-cashier__tabs > div > div.dc-table.buy-sell__table > div.buy-sell__table-body > div > div > div > div:nth-child(1) > div > div').scrollHeight);")
            
            time.sleep(3)         

        





            scroll_height = driver.execute_script("return document.querySelector('#app_contents > div > div > div > div > div.dc-page-overlay__content > div > div.dc-vertical-tab__content.dc-vertical-tab__content--floating > div > main > div > div.dc-tabs__content.dc-tabs__content--p2p-cashier__tabs > div > div.dc-table.buy-sell__table > div.buy-sell__table-body > div > div > div > div:nth-child(1) > div > div').scrollHeight")
            if scroll_height == last_scroll_height:
                break
            else:
                # print("scroll_height",scroll_height)
                # print("last_scroll_height",last_scroll_height)
                last_scroll_height = scroll_height
                pass


    except:
        
        print("Trying Again")
        pass

# def OrderConfirmStatus():

#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[1]/ul/div/li[2]"))).click()
#     print("checking active orders")
#     time.sleep(3)
#     TypeBuy = driver.find_element_by_xpath("//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div")
#     Status = TypeBuy.text

#     if Status == "Buy":
#         print("Truee")
#         return True
        
#     else:
#         print("Falsee")
#         return False
                                            

def active():
    try:
        #driver.get("https://app.deriv.com/cashier/p2p")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[1]/ul/div/li[2]"))).click()
        print("checking active orders")                                         
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dc_inactive_toggle_item']"))).click()
    except:
        try:
            time.sleep(5)
            driver.get("https://app.deriv.com/")
            time.sleep(3)
                        
            
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dt_cashier_tab']/span"))).click()
            #driver.get("https://app.deriv.com/cashier/p2p")
            time.sleep(5)
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dc_dp2-p_link']"))).click()
            time.sleep(5)


        
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[1]/ul/div/li[2]"))).click()
            
            print("checking active orders again")
            
    
        except:
            print("Trying")
            try:
                element = driver.find_element_by_id("dt_login_button")
                print (element.is_enabled())
                loginCHK = element.is_enabled()
                if loginCHK == True:
                    print("login again")
                     
                    playsound.playsound("alert4.wav")
                    time.sleep(5)

                    login()
            except:
                print("some error")
                pass
    
    try:
        time.sleep(3)
        check = driver.find_elements_by_xpath("//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]")
        print("check")   
        # time.sleep(2)
        # check2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]")))
        
        # print("check2: ",check2)  
        status = driver.find_elements_by_xpath("//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[4]/div")
        
        for stat in status:
            O_status = stat.text
            print("status :",O_status)
            if O_status == "Confirm payment":
                for i in range(5):    
                    playsound.playsound("alert3.mp3")



        for order in check:                  
            ID = order.text + '\n'
            print("Order ID: ",ID)

            a_file = open("log.txt", "r")
            list_of_lines = a_file.readlines()
            if ID in list_of_lines:
                print("pass")
                pass

            else:
                print("You have New Order ID: ",ID)
                for i in range(5):    
                    playsound.playsound("alert2.mp3")
                a_file = open("log.txt", "a")
                a_file.writelines(ID)
                a_file.close()


    except:
        print("no Active Order")
        time.sleep(5)    

def internetCheck():
    try:
        requests.get('https://app.deriv.com/').status_code
        print("Connected")
    except:
        print("Not Connected")
        playsound.playsound("alert5.wav")
        time.sleep(3)
        internetCheck()

def main():
    
    #cls()  
    login()  
    #pyautogui.alert(text="Please Add verification code and then press OK ", title='Cookies', button='OK')
    time.sleep(5)
    driver.get("https://app.deriv.com/cashier/p2p")
    
    for trying in itertools.count():
        print("\n")
        print("------------------------------------------------------------------------------------------")
        print("\n")
        
        buy() 
        print("\n")
        print("\n")
        active()

        internetCheck()
        print(" Waiting for {} Sec".format(RefreshTime))
        
        
        time.sleep(RefreshTime)
    
if __name__ == "__main__":
    main()