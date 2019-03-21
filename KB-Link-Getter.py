import time
import requests
import bs4
import selenium
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from collections import OrderedDict

chrome_options = Options()
chrome_options.add_experimental_option("useAutomationExtension", False)
browser = webdriver.Chrome(options=chrome_options)
browser.implicitly_wait(10)
wait = WebDriverWait(browser, 10)
writable_master_list = []
FIRMS = ["Allen Matkins Leck Gamble & Mallory LLP",
         "Arnall Golden & Gregory IS/IT", "Baker Donelson",
         "Butler Snow IS/IT", "Chadbourne & Parke",
         "Cox Castle Nicholson IS/IT", "Dentons Canada",
         "Dentons IS/IT", "Fisher Phillips IS/IT",
         "Franczek Radelet IS/IT", "Gibbons", "Hinshaw & Culbertson IS/IT",
         "Hodgson Russ", "Honigman Miller Schwartz and Cohn",
         "Larkin Hoffman IS/IT", "Mayer Brown Service Desk IS/IT",
         "Maynard Cooper IS/IT", "McAfee & Taft",
         "MGC - McAngus Goudelock & Courie IS/IT",
         "Paul Frank + Collins IS/IT", "Porter Wright IS/IT",
         "Sheppard Mullin", "Thompson Coburn LLP", "Wilson Sonsini IS/IT"]

kb_base_url = "https://app.iqtrack.com/#knowledgebase"
browser.get(kb_base_url)

wait.until(EC.element_to_be_clickable((By.ID, "textfield-1013-inputEl")))

username = browser.find_element_by_id("textfield-1013-inputEl")
password = browser.find_element_by_id("textfield-1014-inputEl")
submit_login = browser.find_element_by_id("button-1016-btnIconEl")

username.send_keys("")
password.send_keys("")
submit_login.click()

for firm in FIRMS:    
    browser.get(kb_base_url)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id,'departmentselector-')]")))
    firm_selector = browser.find_element_by_xpath("//input[contains(@id,'departmentselector-')]")
    search = browser.find_element_by_name("SearchForText")
    #submit = browser.find_element_by_xpath("//span[contains(@id,'button-') and contains(@id,'-btnIconEl')]")


    firm_selector.send_keys("")
    firm_selector.send_keys(str(firm))
    firm_selector.send_keys(Keys.RETURN)
    time.sleep(3)
    search.send_keys("http")
    search.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.XPATH, ".//span[@class='item ']")))
    kb_links = browser.find_elements_by_xpath(".//span[@class='item ']")

    kbs = []
    hyperLinks = []
    textLinks = []
    masterList = []
    tempList = []
    indices = []
    strippedStr = []
    for span in kb_links:
        kbs.append(span.get_attribute('innerHTML'))
        
    for firmLinks in kbs:
        url = "https://app.iqtrack.com/#kbarticle/" + firmLinks
        browser.get(url)
        #wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@id,'button-')]")))
        time.sleep(3)
        title =  browser.find_element_by_xpath("//div[@class='title']").text
        hyperLinks = browser.find_elements_by_xpath("//a[@href]")
        textLinks = browser.find_elements_by_xpath("//*[contains(text(), 'http')]")

        for link in hyperLinks:
            print  (title + " " + link.get_attribute('innerHTML'))
            masterList.append(title + " " + link.get_attribute('innerHTML'))

        for link in textLinks:
            tempList.append(link.get_attribute('innerHTML'))

            for temp in tempList:
                strippedStr = str(temp).split()
                #print (strippedStr)
                indices = [i for i, s in enumerate(strippedStr) if 'http' in s]
                #print (indices)
                for item in indices:
                    strippedStr[item] = re.sub('\(', '', strippedStr[item])
                    strippedStr[item] = re.sub('\)', '', strippedStr[item])
                    strippedStr[item] = re.sub('<br>', '', strippedStr[item])
                    strippedStr[item] = re.sub('<a>', '', strippedStr[item])
                    strippedStr[item] = re.sub('<hr>', '', strippedStr[item])
                    strippedStr[item] = re.sub('<div>', '', strippedStr[item])
                    strippedStr[item] = re.sub('</div>', '', strippedStr[item])
                    strippedStr[item] = re.sub('</br>', '', strippedStr[item])
                    strippedStr[item] = re.sub('</a>', '', strippedStr[item])
                    strippedStr[item] = re.sub('</hr>', '', strippedStr[item])
                    strippedStr[item] = re.sub('<li>', '', strippedStr[item])
                    strippedStr[item] = re.sub('</li>', '', strippedStr[item])
                    strippedStr[item] = re.sub('href=', '', strippedStr[item])
                    strippedStr[item] = re.sub('target=', '', strippedStr[item])
                    strippedStr[item] = re.sub('\"', '', strippedStr[item])
                    
                    tmp = title + " " + strippedStr[item]
                    print (tmp)
                    masterList.append(tmp)

    writable_master_list = list(dict.fromkeys(masterList))
    file = open("firm_links.txt","a")
    file.write("================================================================================\n")
    file.write(str(firm) + "\n")
    file.write("================================================================================\n")
    for item in writable_master_list:
        file.write(str(item) + "\n")
    file.write("================================================================================\n")
    file.write(str(firm) + "\n")
    file.write("================================================================================\n")
    file.close()


#<input id="departmentselector-1031-inputEl" type="text" role="combobox" class="x-form-field x-form-text combobox-editable x-form-focus x-field-form-focus x-field-default-form-focus" autocomplete="off" name="departmentselector-1031-inputEl" spellcheck="false" style="width: 100%;">
#<div class="x-trigger-index-0 x-form-trigger x-form-arrow-trigger x-form-trigger-first" role="presentation" id="ext-gen1200"></div>
#<div class="x-trigger-index-0 x-form-trigger x-form-arrow-trigger x-form-trigger-first" role="presentation" id="ext-gen1200"></div>
#<div class="x-trigger-index-0 x-form-trigger x-form-arrow-trigger x-form-trigger-first x-form-trigger-over x-form-arrow-trigger-over" role="presentation" id="ext-gen1200"></div>
