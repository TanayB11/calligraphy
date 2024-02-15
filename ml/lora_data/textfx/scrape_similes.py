from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome()
driver.implicitly_wait(1)

driver.get("https://textfx.withgoogle.com/")

start_button_div = driver.find_element(By.XPATH, value="/html/body/div[1]/main/div/div[6]/a/button")
start_button_div.click()

sleep(2)

simile_button = driver.find_element(by=By.CSS_SELECTOR, value=".js-macro-Simile > button:nth-child(1) > svg:nth-child(1)")
simile_button.click()

sleep(2)

simile_textbox = driver.find_element(by=By.CSS_SELECTOR, value="._input_15ixm_18")
run_button = driver.find_element(by=By.CSS_SELECTOR, value="._root_1s01q_1")

with open ('./simile_prompts.txt', 'r') as f:
    for line in f.readlines():
        if (len(line.strip()) > 25):
            continue
        simile_textbox.send_keys(Keys.COMMAND,"a")
        simile_textbox.send_keys(Keys.DELETE)
        simile_textbox.send_keys(line.strip())
        run_button.click()

download_button = driver.find_element(by=By.CSS_SELECTOR, value="._actions_14gkr_76 > a:nth-child(1) > svg:nth-child(1)")
sleep(60)

driver.quit()
