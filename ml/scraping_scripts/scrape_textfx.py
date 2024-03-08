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

task_button = driver.find_element(by=By.XPATH, value="/html/body/div[1]/main/div/section/div[2]/div[2]/div/ul/li[8]/button")


task_button.click()

sleep(2)

# task_textbox = driver.find_element(by=By.CSS_SELECTOR, value="._input_15ixm_18")
fuse_textbox1 = driver.find_element(by=By.CSS_SELECTOR, value="li._fieldset_15ixm_77:nth-child(1) > div:nth-child(2) > input:nth-child(1)")
fuse_textbox2 = driver.find_element(by=By.CSS_SELECTOR, value="li._fieldset_15ixm_77:nth-child(2) > div:nth-child(2) > input:nth-child(1)")
run_button = driver.find_element(by=By.CSS_SELECTOR, value="._root_1s01q_1")

with open ('./gpt_prompts/fuse_prompts.txt', 'r') as f:
    for line in f.readlines():
        if (len(line.strip()) > 30):
            continue

        line = line.strip().split()

        fuse_textbox1.send_keys(Keys.COMMAND,"a")
        fuse_textbox1.send_keys(Keys.DELETE)
        fuse_textbox1.send_keys(line[0])

        fuse_textbox2.send_keys(Keys.COMMAND,"a")
        fuse_textbox2.send_keys(Keys.DELETE)
        fuse_textbox2.send_keys(line[1])

        run_button.click()

sleep(300)
download_button = driver.find_element(by=By.CSS_SELECTOR, value="._actions_14gkr_76 > a:nth-child(1)")
sleep(300)

driver.quit()
