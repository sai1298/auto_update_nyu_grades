
import csv
from selenium import webdriver
from click_on_course import brightspace_search
from lab_grades import *
import time
from brightspace_login import *

def split_names(names):
    """Split 'Jain; Jack ' → ['Jain', 'Jack']."""
    return [name.strip() for name in names.split(",") if name.strip()]

def split_usernames(usernames):
    """Split 'ljsj; jjwj7' → ['ljwwwq2', 'hfhfk22']."""
    return [u.strip() for u in usernames.split(",") if u.strip()]

  # ← change to your .csv file name
# count =0
def update_student_details(driver,student_name,grade,student_feedback):
    try:
        brightspace_search(driver, student_name, timeout=20)
        update_details(grade,student_feedback,driver)
        time.sleep(5)
        home_page(driver)
    except:
        pass

def get_stud_grades(driver=None):
    csv_file = "/Users/sairampurimetla/Desktop/VLSI_GRades/lab5.csv" 
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            # Extract fields
            names = split_names(row["Names"])
            # usernames = split_usernames(row["Usernames"])
            # total = row["Grade"]
            # checkout = row["CheckoutScore"]
            final_total = row["lab5 marks"]
            # comments = row["Comments"]
            final_comments = row["comments"]

            # Print individual info
            for name in names:
                # print("-----------------------------------------------------")
                print(f"Student: {name}")
                # print(f"Total Score: {total}")
                # print(f"Checkout Score: {checkout}")
                # print(f"Final Total: {final_total}")
                # # print(f"Comments: {comments if comments else '—'}")
                # print(f"Final Comments: {final_comments if final_comments else '—'}")
                # print("-----------------------------------------------------\n")
                print(name,final_total,final_comments)
                update_student_details(driver,name,final_total,final_comments)
                # count+=1




def home_page(driver):
    # Always reset context back to the main document
    driver.switch_to.default_content()
    # Reload the grading/submissions page
    driver.get(SUBMISSION_URL)


# Example usage:
if __name__ == "__main__":
    driver = webdriver.Chrome()
    SUBMISSION_URL = "https://brightspace.nyu.edu/d2l/lms/dropbox/admin/mark/folder_submissions_users.d2l?db=1104645&ou=500446"
    driver.get(SUBMISSION_URL)  # or the Brightspace redirect URL

    login_nyu_microsoft(driver)
    condition = input("enter user input:")
    get_stud_grades(driver)
    time.sleep(5)
    condition = input("enter user input:")
    # Reload the grading/submissions page
    driver.quit()