from selenium import webdriver
import time
import csv, re

import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import itertools
import playsound


url = "https://app.deriv.com/"
driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)
cls = lambda: os.system('cls')


# with open("login_info.txt", 'r', encoding='utf-8-sig') as csv_file:
       
#         csv_reader = csv.reader(csv_file, delimiter=";")
a_file = open("login_info.txt", "r")
list_of_lines = a_file.readlines()
#for line in list_of_lines:
        # for line in csv_reader:
mail = list_of_lines[0]
password = list_of_lines[1]
Condition1 = int(list_of_lines[2]) # rate
Condition2 = int(list_of_lines[3]) # usd limit
BankBalance = int(list_of_lines[4]) # BankBalance
RefreshTime =  int(list_of_lines[5])

    


print('Remaning Balance : ',BankBalance)

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
            
            element = driver.find_element_by_id("dt_login_button")
            print (element.is_enabled())
            loginCHK = element.is_enabled()
            if loginCHK == True:
                
                time.sleep(5)
                login()
          
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
        # start
        print('Condition 1 $ rate less than  ',Condition1)
        print('Condition 2  limit greater than ',Condition2)
        while True:
            rate3 = driver.find_elements_by_xpath("//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div[3]/span")        
           # print("rate3",rate3)
            key = 1
            for i in rate3:    
                a_file = open("login_info.txt", "r")
                list_of_lines = a_file.readlines()
                BankBalance = int(list_of_lines[4]) # BankBalance
               # print('BankBalance Balance : ',BankBalance)                     
                #print("rate3",i.text)  
                num = i.text
                num2 = list(re.split(" ", num))
                USDRate = int(float(num2[0]))

                if USDRate <=Condition1:
                
                    string = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[2]".format(key)               
                    rate2 = driver.find_element_by_xpath(string).text          
                    num3 = list(re.split(" |–", rate2))               
                    USDLimit = int(float(num3[1]))
                    if USDLimit >= Condition2:

                        if BankBalance > float(num2[0])*float(num3[1]):
                            
                            string2 = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[1]/div/div[2]/div".format(key)
                            BuyButt = "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[{}]/div/div/div/div/div[4]/button".format(key)
                            
                            name = driver.find_element_by_xpath(string2).text
                            if name == "Invita":
                                print("name:Invita:::", name)
                                pass
                            
                            else:
                                print('These name have your offer condition true:   ',name)
                                print('Condition 1: ',USDRate)
                                print('Condition 2: ',USDLimit)
                                print('Condition 3: BankBalance = {} > Condition1 X Condition2 ={} '.format(BankBalance, float(num2[0])*float(num3[1])))
                                driver.find_element_by_xpath(BuyButt).click()
                                time.sleep(2)
                                driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(Keys.CONTROL, 'a')
                                time.sleep(1)
                                driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(Keys.BACKSPACE)
                                time.sleep(2)
                                driver.find_element_by_xpath("//*[@id='modal_root']/div/div/div[2]/div/form/div/div[3]/div[1]/div[1]/input").send_keys(USDLimit)
                                time.sleep(1)
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='modal_root']/div/div/div[3]/div/button[2]"))).click()
                                for i in range(5):    
                                    playsound.playsound("alert.wav")
                                
                                
                                
                            
                                BankBalance_new = BankBalance - (float(num2[0])*float(num3[1]))
                                print('Remaning Balance : ',BankBalance_new)
                                a_file = open("login_info.txt", "r")
                                list_of_lines = a_file.readlines()
                                list_of_lines[4] =  "{}\n".format(int(BankBalance_new))
                                
                                a_file = open("login_info.txt", "w")
                                a_file.writelines(list_of_lines)
                                a_file.close()
                                #pyautogui.alert(text="Please Click OK after verifying that order and new bankBalance is correct  ", title='Cookies', button='OK')
                                time.sleep(5)
                                driver.get("https://app.deriv.com/cashier/p2p")
                                time.sleep(3)
                                buy()
                            

                key += 1
                
            driver.execute_script("document.querySelector('#app_contents > div > div > div > div > div.dc-page-overlay__content > div > div.dc-vertical-tab__content.dc-vertical-tab__content--floating > div > main > div > div.dc-tabs__content.dc-tabs__content--p2p-cashier__tabs > div > div.dc-table.buy-sell__table > div.buy-sell__table-body > div > div > div > div:nth-child(1) > div > div').scrollTo(0, document.querySelector('#app_contents > div > div > div > div > div.dc-page-overlay__content > div > div.dc-vertical-tab__content.dc-vertical-tab__content--floating > div > main > div > div.dc-tabs__content.dc-tabs__content--p2p-cashier__tabs > div > div.dc-table.buy-sell__table > div.buy-sell__table-body > div > div > div > div:nth-child(1) > div > div').scrollHeight);")
            #driver.execute_script("window.scrollTo(0, document.querySelector('#app_contents > div > div > div > div > div.dc-page-overlay__content > div > div.dc-vertical-tab__content.dc-vertical-tab__content--floating > div > main > div > div.dc-tabs__content.dc-tabs__content--p2p-cashier__tabs > div > div.dc-table.buy-sell__table > div.buy-sell__table-body > div > div > div > div:nth-child(1) > div > div').scrollHeight);")
            
            time.sleep(3)                                   


            #  end

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
                        
            element = driver.find_element_by_id("dt_login_button")
            print (element.is_enabled())
            loginCHK = element.is_enabled()
            if loginCHK == True:
                
                time.sleep(5)
                login()
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dt_cashier_tab']/span"))).click()
            #driver.get("https://app.deriv.com/cashier/p2p")
            time.sleep(5)
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dc_dp2-p_link']"))).click()
            time.sleep(5)


        
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[1]/ul/div/li[2]"))).click()
            
            print("checking active orders again")
    
        except:
            print("some error")
            pass
    
    try:
        time.sleep(3)
        check = driver.find_elements_by_xpath("//*[@id='app_contents']/div/div/div/div/div[2]/div/div[2]/div/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]")
        print("check: ",check)   
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

def main():
    
    #cls()  
    login()  
    #pyautogui.alert(text="Please Add verification code and then press OK ", title='Cookies', button='OK')
    time.sleep(5)
    driver.get("https://app.deriv.com/cashier/p2p")
    for trying in itertools.count():
        buy() 
        
        active()
        print(" Waiting for {} Sec".format(RefreshTime))
        
        time.sleep(RefreshTime)
    
if __name__ == "__main__":
    main()
