import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

email = "temitopeoluwabunmi4@gmail.com" #input("enter your mail: ")
password = "12345678"

MUINITE = 60


class URL:
    LOGIN = "https://ogsera.ogunstate.gov.ng/login"
    DASHBOARD = "https://ogsera.ogunstate.gov.ng/dashboard"
    BROADSHEET = "https://ogsera.ogunstate.gov.ng/result/admin/broadsheet2" 
    
    
class PATHS:
    TERM = "/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[1]/div[1]/div/select"
    PROGRAMME="/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[1]/div[2]/div/select"
    CLASSNAME="/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[1]/div[3]/div/select"
    LOADING_FOR_SELECTING_CLASS = "/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[2]"
    BROADSHEET_TABLE="/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div/div/div[3]/div"
    GET_SCORE = lambda row, column : f"/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div/div/div[3]/div/div/section/table/tr[{row}]/td[{column}]"
    GET_ALL_EL_IN_ROW = lambda row : f"/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div/div/div[3]/div/div/section/table/tr[{row}]/td"
    GET_ALL_EL_ROWS = "/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div/div/div[3]/div/div/section/table/tr"
    COMMENT_INPUT = "/html/body/div[2]/div[1]/div/div/div/div/form/div[1]/div/input"
    SUBMIT_COMMENT= "/html/body/div[2]/div[1]/div/div/div/div/form/div[2]/button[1]"


driver = webdriver.Chrome()
wait = WebDriverWait(driver, MUINITE * 10)
action = ActionChains(driver)


def find_el(str):
    return driver.find_element(by=By.XPATH, value=str)

def find_multi_el(str):
    return driver.find_elements(by=By.XPATH, value=str)

def wait_for_correct_current_url(desired_url):
    wait.until(
        lambda driver: driver.current_url == desired_url)
    
def scroll_to(element):
    action.move_to_element(element).perform()

driver.get(URL.LOGIN)
driver.find_element(by=By.ID, value="authEmailInput").send_keys(email)
driver.find_element(by=By.ID, value="authPasswordInput").send_keys(password)
driver.find_element(by=By.CSS_SELECTOR, value="button.btn.btn-primary.btn-lg").submit()

wait_for_correct_current_url(URL.DASHBOARD)
time.sleep(5)
driver.get(URL.BROADSHEET)
wait_for_correct_current_url(URL.BROADSHEET)

# values are PRI, NUR, KIN
# find_el(PATHS.TERM).send_keys("2024/2025 First Term")
# time.sleep(5)
# find_el(PATHS.PROGRAMME).send_keys("PRI")
# time.sleep(5)
# find_el(PATHS.CLASSNAME).send_keys("PRI 6") # this should be a loop
wait.until(lambda driver: len(driver.find_elements(by=By.XPATH, value=PATHS.BROADSHEET_TABLE)) > 0 )

TOTAL_ROWS =len(find_multi_el(PATHS.GET_ALL_EL_ROWS)) + 1
for current_row in range(TOTAL_ROWS):
    if current_row < 47:
        continue
    # current_row = 3
    all_columns = find_multi_el(PATHS.GET_ALL_EL_IN_ROW(current_row))
    length = len(all_columns)


    if (TOTAL_ROWS - 5) <= current_row:
        time.sleep(10) 

    try:
        cummulative = all_columns[-7]
        scroll_to(cummulative)
        students_cumulative = cummulative.text
        # print('cummulative',cummulative.text, flush=True)
        c = float(students_cumulative)
        time.sleep(5)
    except:
        cummulative_list = []
        # print("length",length, flush=True)
        for index in range(length):
            count = index + 1
            if count % 4 == 0:
                try:
                    scroll_to(all_columns[index])
                    # print(count, index, all_columns[index].text, flush=True)
                    cummulative_list.append(float(all_columns[index].text))
                except:
                    continue
        try:
            c = sum(cummulative_list) / len(cummulative_list)
        except:
            continue
        # print('calculated',c, flush=True)
        time.sleep(2)

    comment_action = all_columns[-1] #for selecting head teacher
    try:
        scroll_to(find_multi_el(PATHS.GET_ALL_EL_IN_ROW(current_row + 1))[-1]) # to scroll into screen
    except:
        scroll_to(comment_action)
    time.sleep(2)
    try:
        dropdown = comment_action.find_element(by=By.CLASS_NAME, value='dropdown')
        dropdown.click()
    except:
        try:
            try: 
                scroll_to(find_multi_el(PATHS.GET_ALL_EL_IN_ROW(current_row + 2))[-1]) 
            finally:
                dropdown = driver.find_element(by=By.XPATH, value=f"/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div/div/div[3]/div/div/section/table/tr[{current_row}]/td[{length}]/div" )
                dropdown.click()
        except:
            
            dropdown = driver.find_element(by=By.XPATH, value=f"/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div/div/div[3]/div/div/section/table/tr[{current_row}]/td[{length}]/div/button" )
            dropdown.click()
    time.sleep(5)
    try:
        dropdown.find_element(by=By.TAG_NAME, value='ul').find_element(by=By.TAG_NAME, value='button').click()
    except:
        driver.find_element(by=By.XPATH, value=f"/html/body/div/div/div[3]/div[1]/div/div/div[2]/div[3]/div/div/div[3]/div/div/section/table/tr[{current_row}]/td[{length}]/div/ul/button" ).click()
    wait.until(lambda driver: len(driver.find_elements(by=By.XPATH, value=PATHS.COMMENT_INPUT)) > 0 )
    comment_el = find_el(PATHS.COMMENT_INPUT)
    comment_el.clear()
    time.sleep(2)


    # try: 
    
    if c >= 70:
        text = "Excellent performance"
    elif c >= 50:
        text = "Satisfactory" 
    elif c >= 40:
        text = "You can do better"
    elif c >= 30:
        text = "Poor performance, sit up."
    else:
        text = "Very weak performance, be steady at class work"
    comment_el.send_keys(text)
    time.sleep(1)
    find_el(PATHS.SUBMIT_COMMENT).click()
    wait.until(lambda driver: len(driver.find_elements(by=By.XPATH, value=PATHS.GET_ALL_EL_IN_ROW(current_row))) > 0 )
    
time.sleep(5000)
driver.close()