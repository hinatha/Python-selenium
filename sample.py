from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging
import csv
import datetime

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

wait = WebDriverWait(driver=driver, timeout=15)

url = "https://www.hiryu.co.jp/"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located)

    more = driver.find_elements_by_class_name("btn")
    more[0].click()

    wait.until(EC.presence_of_all_elements_located)
    print("Open more topics")
    print("Execute open csv file")
    csv_date = datetime.datetime.today().strftime("%Y%m%d")
    csv_file_name = "hiryu_topic_" + csv_date + ".csv"
    f = open(csv_file_name, "w", encoding="CP932", errors="ignore")
    
    writer = csv.writer(f, lineterminator="\n") 
    csv_header = ["id","title","URL"]
    writer.writerow(csv_header)

    i = 0
    item = 1
    while True:
        i = i + 1
        print(i)
        wait.until(EC.presence_of_all_elements_located)
        for elem_a in driver.find_elements_by_xpath('//dd/a'):
            csvlist = []
            csvlist.append(str(item))
            csvlist.append(elem_a.text)
            csvlist.append(elem_a.get_attribute('href'))
            writer.writerow(csvlist)
            item = item + 1
        if i > 4:
            break
        next_link = driver.find_element_by_css_selector(".next.page-numbers")
        driver.get(next_link.get_attribute('href'))
    
    f.close()
    print("Finished")
except Exception as err:
        '''
        Execute except
        https://docs.python.org/ja/3/tutorial/errors.html
        '''
        rc = 1
        logger.error(f'''An exception occured. [RETURN CODE: {rc}][ERROR: {err}]''')
        '''
        Execute raise Exception
        https://uxmilk.jp/39845
        '''
        raise Exception((f'''An exception occured. [RETURN CODE: {rc}][ERROR: {err}]'''))
finally:
    driver.close()
    driver.quit()
