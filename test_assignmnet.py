import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_driver_path = "D:\Personal\chromedriver.exe"
options = Options()
service = Service(chrome_driver_path)

# Initialize the WebDriver with the service
driver = webdriver.Chrome(service=service, options = options)

# Navigate to the Fitpeo home page
driver.get("https://www.fitpeo.com/")
driver.maximize_window()
#pdb.set_trace()
driver.implicitly_wait(20)

# Navigate to the revenue calculator page
driver.find_element(By.XPATH, "//div[contains(text(),'Revenue Calculator')]").click()
time.sleep(5)
driver.switch_to.default_content()

# source_MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary css-1sfugkh"]')
slider = driver.find_element(By.XPATH, '//input[@type="range"]')
driver.execute_script("arguments[0].scrollIntoView(true);",slider)
time.sleep(10)
slider_width = slider.size['width']
min_value = int(slider.get_attribute('min'))
max_value = int(slider.get_attribute('max'))

# Calculate the target offset
target_value = 820
slider_value = int(slider.get_attribute('value'))
offset = (target_value - slider_value) / (max_value - min_value) * slider_width

driver.execute_script("arguments[0].value = arguments[1];", slider, target_value)

actions = ActionChains(driver)
actions.click_and_hold(slider).move_by_offset(offset,0).release().perform()

time.sleep(10)
#  Get the slider value and assert it's correct
slider_value = driver.find_element(By.XPATH, '//input[@type="number"]').get_attribute('value')
assert slider_value == '236', f"Expected slider value 236, but got {slider_value}"
print(slider_value,'##########')

text_field = driver.find_element(By.XPATH, '//input[@type="number"]')
# Update the text field
text_field.clear()
time.sleep(5)
text_field.click()
text_field.send_keys("236")
time.sleep(5)

# Get the updated slider value and assert it's correct
updated_slider_value = driver.find_element(By.XPATH, '//input[@type="number"]').get_attribute('value')
assert updated_slider_value == '236', f"Expected updated slider value 236, but got {updated_slider_value}"
print(updated_slider_value,'$$$$$$$$$$')

# Scroll down to select CPT Codes
driver.execute_script("window.scrollBy(0, 300);")

# Wait for CPT code checkboxes to be clickable
cpt_codes = [
    '(//input[@class="PrivateSwitchBase-input css-1m9pwf3"])[1]',
    '(//input[@class="PrivateSwitchBase-input css-1m9pwf3"])[2]',
    '(//input[@class="PrivateSwitchBase-input css-1m9pwf3"])[3]',
    '(//input[@class="PrivateSwitchBase-input css-1m9pwf3"])[4]'
]

for code in cpt_codes:
    time.sleep(5)
    checkbox = driver.find_element(By.XPATH, code)
    if not checkbox.is_selected():
        checkbox.click()

# Close the browser after the test
driver.quit()