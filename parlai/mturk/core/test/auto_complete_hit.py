# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
"""
Script for auto-completing HITs. Please change the test flow according to your task.
"""
try:
    from selenium import webdriver
    import chromedriver_installer
except ModuleNotFoundError:
    raise SystemExit("Please make sure your computer has Chrome installed, and then install selenium and chromedriver by running: pip install selenium chromedriver_installer")
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import sys
import time
import random

HIT_page_url = sys.argv[1]

# create a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()

# login to your MTurk sandbox account
print("Please log into your MTurk sandbox account within 10 minutes...")
driver.get("https://workersandbox.mturk.com/mturk/beginsignin")
while not "Sign Out" in driver.page_source:
    time.sleep(1)
print("Successfully logged into your MTurk sandbox account.")

# navigate to the HIT page
driver.get(HIT_page_url)

total_hits_done = 0

while not "There are no HITs in this group available to you at the moment." in driver.page_source:
    # Click "Accept" button
    wait = WebDriverWait(driver, 30)
    accept_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '''#cookieDependentFunctionality > input[type="image"]''')))
    print("Clicking on Accept button...")
    accept_button.send_keys("\n")        
     
    # Wait for main page to show up
    iframe = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > form > iframe")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.switch_to.frame(iframe)
    
    # Send message
    for i in range(50):
        print("Sending message...")
        input_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#id_text_input")))
        input_box.send_keys("text to send")
        #input_box.send_keys(Keys.RETURN)
        send_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#id_send_msg_button")))
        send_button.click()
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#id_text_input")))

    # Click "Done with this HIT" button
    wait = WebDriverWait(driver, 30)
    done_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#done-button")))
    print("Clicking on Done button...")
    done_button.click()
    total_hits_done += 1
    print("Total HITs done: " + str(total_hits_done))
    print("\n")

    print("Going to next HIT...")
    driver.get(sys.argv[1])

print("All HITs are done!")
driver.quit()