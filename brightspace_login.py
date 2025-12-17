from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from click_on_course import brightspace_search
from lab_grades import *


NETID = ""                  # your NetID
PASSWORD = ""   # <-- replace securely
NETID_EMAIL = f"{NETID}@nyu.edu"

def login_nyu_microsoft(driver, timeout=20):
    netid_email, password = NETID_EMAIL , PASSWORD

    wait = WebDriverWait(driver, timeout)

    # --- 1) Enter username (NetID email) ---
    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, "i0116"))  # or (By.NAME, "loginfmt")
    )
    username_input.clear()
    username_input.send_keys(netid_email)

    next_button = wait.until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))
    )
    next_button.click()

    # Optional: small pause if the page is slow
    # time.sleep(3)

    # --- 2) Enter password ---
    pwd_box = wait.until(
        EC.visibility_of_element_located((By.NAME, "passwd"))  # or (By.ID, "i0118")
    )
    pwd_box.clear()
    pwd_box.send_keys(password)

    sign_in_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))
    )
    sign_in_btn.click()

#####]sssssss



# def home_page(driver):
#     # Always reset context back to the main document
#     driver.switch_to.default_content()
#     # Reload the grading/submissions page
#     driver.get(SUBMISSION_URL)

# def update_student_details(driver,student_name,grade,student_feedback):
#     try:
#         brightspace_search(driver, student_name, timeout=20)
#         update_details(grade,student_feedback,driver)
#         home_page(driver)
#     except:
#         pass










