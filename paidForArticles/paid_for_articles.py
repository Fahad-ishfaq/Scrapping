from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
from bs4 import BeautifulSoup
import time, random, json
from datetime import datetime
from resource.keyword import KEYWORDS, COUNTRY_LIST

DEBUG = False
username = os.getenv("USERNAME")
userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir={}".format(userProfile))
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
chrome_options.add_argument("--disable-blink-features")# for web which  detectcts bot
chrome_options.add_argument("--disable-blink-features=AutomationControlled")# # for web which  detectcts bot
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])


# ===========================================================
# Utils/
# ===========================================================

def get_category(counter):
    categories = open("resource/categories.txt", "r")
    category_list =  categories.readlines()
    # print(category_list, len(category_list))
    if counter  <= len(category_list):
        category = category_list[counter].replace('\n',"")
        return category
    else:
        return None

def get_credentials(site):
    credentails = open("resource/login.txt", "r")
    credentails_list = credentails.readlines()
    if site == "rytr":
        list_ = credentails_list[1].replace("\n","").split(",")
    elif site == "articles":
        list_ = credentails_list[3].replace("\n","").split(",")
    else:
        list_ = [None, None]
    return list_[0], list_[1]

def get_old_questions():
    with open("resource/log.json", "r") as f:
        questions_dic=json.load(f)
    return questions_dic

def add_new_answered_questions(all_questions):
    with open("resource/log.json", "w") as f:
        f.write(json.dumps(all_questions))
    return True

# ===========================================================
# Drivers Utils/
# ===========================================================

def get_new_driver(url, chrome_options = None):
    if chrome_options:
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
            })
    else:
        driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)
    return driver


def switch_to_default_or_frame(driver, frame=None):
    if frame:
        driver.switch_to_frame(frame)
    else:
        driver.switch_to_default_content()
        driver.switch_to_default_content
    return driver

def start_all_drivers():
    driver = get_new_driver("https://google.com/", chrome_options)
    driver_rytr = get_new_driver("https://rytr.me/")
    driver_articles = get_new_driver("https://paidforarticles.com/")
    return driver, driver_rytr, driver_articles


# ===========================================================
# Google Driver/
# ===========================================================

def generate_new_question_list(driver, category):
    new_questions_list = []
    google_url = "https://www.google.com/search?q="
    question = category + " people also ask"
    driver.get((google_url+question))
    time.sleep(4)
    try:
        for i in range(0,5):
            driver.find_elements_by_xpath('//div[@jsname="F79BRe"]')[i].click()
            time.sleep(2)

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        questions_list = soup.select('[jsname="jIA8B"] span')
        for question in questions_list:
            new_questions_list.append(question.text)
        return new_questions_list

    except Exception as e:
        print("No Questions found.\n\nError:",e)
        return new_questions_list

def search_country_trend(driver, url):
    trend_list=[]
    driver.get(url)
    time.sleep(5)

    while(True):
        try:
            driver.find_element_by_xpath("//*[@ng-click='ctrl.loadMoreFeedItems()']").click()
            time.sleep(5)
        except:
            break

    try:
        trends=driver.find_elements_by_xpath('//*[@ng-attr-title]')
    except:
        trends = []
    for trend in trends:
        try:
            if trend.text.strip!='':
                trend_list.append(trend.text)
        except:
            pass
    return trend_list

def get_google_keywords(driver, category, c_list):
    trend_list=[]
    if c_list == [] or c_list == None or DEBUG:
        c_list =  ["US", "GB"]

    if category=="Tech" or category=="Science":
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=t"
    elif category=="Sports":
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=s"
    elif category=="Business":
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=b"
    elif category=="Lifestyle" or category=="Entertainment":
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=e"
    elif category=="Health":
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=m"
    elif category=="News":
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=h"
    elif category=="Education":
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=all"
    else:
        url="https://trends.google.com/trends/trendingsearches/realtime?geo={}&category=all"


    for name in c_list:
        time.sleep(10)
        new_url=url.format(name)
        trend_list+=search_country_trend(driver, new_url)
    return trend_list

# ===========================================================
# Ryte Driver/
# ===========================================================

def login_rytr(driver_rytr):
    email, password = get_credentials("rytr")
    driver_rytr.get("https://rytr.me/")
    time.sleep(3)
    driver_rytr = switch_to_default_or_frame(driver_rytr)
    time.sleep(3)
    driver_rytr.find_element_by_css_selector(".style_button___8d0M.style_default__8UJG6.style_large__84rWD").click()
    time.sleep(6)
    iframe = driver_rytr.find_element_by_css_selector("iframe")
    driver_rytr = switch_to_default_or_frame(driver_rytr, iframe)
    time.sleep(6)
    # continute with email
    driver_rytr.execute_script('document.getElementsByClassName("style_button__SHA7S style_white__2yF4x style_medium__CsYAK")[3].click()')
    driver_rytr.find_element_by_name("email").send_keys(email)
    driver_rytr.find_element_by_css_selector(".style_button__SHA7S.style_primary__aA3ci.style_medium__CsYAK").click()
    time.sleep(6)
    driver_rytr.find_element_by_name("password").send_keys(password)
    driver_rytr.find_element_by_css_selector(".style_button__SHA7S.style_primary__aA3ci.style_medium__CsYAK").click()
    return driver_rytr
    # Login end

# # selecting element by blog idea

def generate_ai_content(driver_rytr, question, blog_select=None):
    if DEBUG:
        stringData = "Technology has evolved and shaped our workplaces in many ways,"
        stringData += "through the adoption of tools like the internet and email for communications,"
        stringData += "word processing, spreadsheets and presentations for office productivity,"
        stringData += "electronic databases for record keeping, and robots and artificial intelligence"
        stringData += "through the adoption of tools like the internet and email for communications,"
        stringData += "word processing, spreadsheets and presentations for office productivity,"
        stringData += "electronic databases for record keeping, and robots and artificial intelligence"
        return stringData

    if blog_select:
        driver_rytr.find_element_by_id("select-type").click()
        time.sleep(2)
        driver_rytr.find_element_by_xpath('//div[@data-valuetext="Blog Section Writing"]').click()
        # Retyring, clearing output div and input and asking new question
    try:
        driver_rytr.find_element_by_xpath("//textarea[@placeholder='Role of AI Writers in the Future of Copywriting']").clear()
        driver_rytr.find_element_by_xpath("//textarea[@placeholder='Role of AI Writers in the Future of Copywriting']").send_keys(question)
        time.sleep(1)
        driver_rytr.find_element_by_css_selector(".style_button__SHA7S.style_primary__aA3ci.style_medium__CsYAK").click()
        time.sleep(6)

        generated_text = driver_rytr.find_element_by_xpath('//div[@contenteditable="true"]').text
        driver_rytr.execute_script('''document.querySelector("div [contenteditable='true']").innerHTML=""''')
    except:
        time.sleep(16)
        try:
            generated_text = driver_rytr.find_element_by_xpath('//div[@contenteditable="true"]').text
            driver_rytr.execute_script('''document.querySelector("div [contenteditable='true']").innerHTML=""''')
        except:
            return None
    return generated_text


# ===========================================================
# Paid for articles/
# ===========================================================

def login_paid_for_articles(driver_articles):
    email, password = get_credentials("articles")
    login_url = "https://paidforarticles.com/login"
    driver_articles.get(login_url)
    time.sleep(5)
    current_url = driver_articles.current_url

    if current_url == login_url:
        driver_articles.find_element_by_id("email").send_keys(email)
        driver_articles.find_element_by_id("password").send_keys(password)
        driver_articles.find_element_by_id("password").send_keys(Keys.ENTER)
        return True
    else:
        return True

def start_new_article(driver_articles, title, category, summary):
    driver_articles.get("https://paidforarticles.com/member/articles/create")
    driver_articles.switch_to_default_content()
    driver_articles.find_element_by_id("title").send_keys(title)
    time.sleep(4)
    try:
        article_category_select = Select(driver_articles.find_element_by_id("category"))
        article_category_select.select_by_visible_text(category)
    except Exception as e:
        print("Category select failed")
    driver_articles.find_element_by_id("summary").send_keys(summary)
    driver_articles.find_element_by_id("reason").send_keys("This is 100% my original content.")
    return True

def write_article_body(driver_articles, heading, text):
    driver_articles = switch_to_default_or_frame(driver_articles)
    article_body = driver_articles.find_element_by_id("content_ifr")
    driver_articles = switch_to_default_or_frame(driver_articles, article_body)
    try:
        driver_articles.execute_script(f'''var para = document.createElement("p");
                                        var heading = document.createElement("strong");
                                        heading.innerHTML = " {heading}";
                                        para.appendChild(heading)
                                        document.getElementById("tinymce").appendChild(para)''')
    except Exception as e:
        print(e)
    for line in text.split("\n"):
        try:
            driver_articles.execute_script(f'''var para = document.createElement("p");
                                        para.innerHTML = " {line}"
                                        document.getElementById("tinymce").appendChild(para)''')
        except Exception as e:
            print(e)

def add_article_image(driver_articles, image_url):
    driver_articles = switch_to_default_or_frame(driver_articles)
    article_body = driver_articles.find_element_by_id("content_ifr")
    driver_articles = switch_to_default_or_frame(driver_articles, article_body)
    driver_articles.execute_script(f'''var para = document.createElement("p");
                                    var image = document.createElement("img");
                                    var br = document.createElement("br")
                                    image.src="{image_url}";
                                    para.appendChild(image)
                                    para.appendChild(br)
                                    document.getElementById("tinymce").appendChild(para)''')

def submit_article(driver_articles):
    try:
        driver_articles = switch_to_default_or_frame(driver_articles)
        time.sleep(4)
        driver_articles.execute_script('''
                            document.getElementsByClassName("btn btn-primary save-article float-right")[0].disabled = false
                            document.getElementsByClassName("btn btn-primary save-article float-right")[0].click()''')
        time.sleep(10)
        if driver_articles.current_url == "https://paidforarticles.com/member/articles":
            return True
        return False
    except Exception as e:
        print("Submit articale exception", e)
        return False

# ===========================================================
# Main/
# ===========================================================

def main():
    if DEBUG:
        print("Warning!!!!!!!!!!!!!!\n\n Debug mode is ON")
    google_driver, driver_rytr, driver_articles = start_all_drivers()

    while True:
        try:
            login_rytr(driver_rytr)
            print("rytr login success")
            break
        except:
            print("rytr login failer \n Trying again!!")

    while True:
        try:
            login_paid_for_articles(driver_articles)
            print("PaidForArticles login success")
            break
        except:
            print("PaidForArticles login failer \n Trying again!!")

    counter = 0
    while True:
        category = get_category(counter)
        google_keywords=get_google_keywords(google_driver, category, COUNTRY_LIST)
        old_questions=get_old_questions()

        NewArticle = True
        article_words=0
        for keyword in google_keywords:
            print(category, keyword)
            ask=keyword + ' ' + category
            questions = generate_new_question_list(google_driver, ask)

            # Generating data for each question
            for question in questions:

                if NewArticle:
                    print("\nStarting New Article\n")
                    summary = generate_ai_content(driver_rytr, questions[0], True)
                    start_article_status = start_new_article(driver_articles, questions[0], category, summary)
                    article_words=0
                    if start_article_status:
                        image_urls=KEYWORDS[category]['images']
                        choose=random.randint(0,len(image_urls)-1)
                        add_article_image(driver_articles, image_urls[choose])
                        NewArticle = False


                if question not in old_questions:
                    old_questions[question]=True
                    text = generate_ai_content(driver_rytr, question)

                    if text is not None and text != '':
                        article_words+=(text.count(" ")+1)
                        write_article_body(driver_articles, question, text)
                    else:
                        print("No text copied")

                if article_words > 900:
                    add_article_image(driver_articles, image_urls[choose])
                    submit = submit_article(driver_articles)
                    if submit:
                        add_new_answered_questions(old_questions)
                        NewArticle = True
                        continue
                    else:
                        print("Article not submitted")

                    time.sleep(5)

            print("Getting New category")

        counter += 1
        if counter>=10:
            break

if __name__ == "__main__":
    today = datetime.today()
    next_week = datetime(2022,4,27)
    if today<next_week:
        main()
    else:
        print("Failed to execute script")
