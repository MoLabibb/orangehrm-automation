from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import re
import time


class AdminPage(BasePage):

    # --- Locators ---
    admin_tab = (By.XPATH, "//span[text()='Admin']")
    records_label = (By.XPATH, "//div[contains(@class,'orangehrm-horizontal-padding')]//span")
    add_button = (By.XPATH, "//button[normalize-space()='Add']")

    # Add User Form
    user_role_dropdown = (By.XPATH, "//label[text()='User Role']/following::div[contains(@class,'oxd-select-text')][1]")
    employee_name_input = (By.XPATH, "//label[text()='Employee Name']/following::input[1]")
    status_dropdown = (By.XPATH, "//label[text()='Status']/following::div[contains(@class,'oxd-select-text')][1]")

    username_field = (By.XPATH, "//label[text()='Username']/following::input[1]")
    password_field = (By.XPATH, "//label[text()='Password']/following::input[@type='password'][1]")
    confirm_password_field = (By.XPATH, "//label[text()='Confirm Password']/following::input[@type='password'][1]")
    save_button = (By.XPATH, "//button[@type='submit']")

    # Search
    search_username_input = (By.XPATH, "//div[label[text()='Username']]/following-sibling::div//input")
    search_button = (By.XPATH, "//button[@type='submit']")

    # Delete
    confirm_delete_btn = (By.XPATH, "//button[contains(.,'Yes, Delete')]")

    # ---------------------------------------------------

    def go_to_admin(self):
        self.click(self.admin_tab)

    # ---------------------------------------------------

    def get_record_count(self):
        self.wait.until(EC.visibility_of_element_located(self.records_label))
        text = self.get_text(self.records_label)

        match = re.search(r"\d+", text)
        if match:
            return int(match.group())
        else:
            print("⚠️ No numeric record count found in label:", text)
            return 0

    # ---------------------------------------------------

    def add_user(self, partial_emp_name, new_username, password):

        self.click(self.user_role_dropdown)
        self.click((By.XPATH, "//div[@role='option']//span[text()='Admin']"))

        self.enter_text(self.employee_name_input, partial_emp_name)
        suggestion = (By.XPATH, "//div[@role='option']//span")
        self.wait.until(EC.visibility_of_element_located(suggestion)).click()

        self.click(self.status_dropdown)
        self.click((By.XPATH, "//div[@role='option']//span[text()='Enabled']"))

        self.enter_text(self.username_field, new_username)
        self.enter_text(self.password_field, password)
        self.enter_text(self.confirm_password_field, password)

        time.sleep(1)
        self.click(self.save_button)

        # Wait until redirected to user list
        self.wait.until(EC.presence_of_element_located(self.search_username_input))

    # ---------------------------------------------------

    def delete_user(self, username):

        # Search for specific username
        search_box = self.wait.until(
            EC.visibility_of_element_located(self.search_username_input)
        )
        search_box.clear()
        search_box.send_keys(username)

        self.click(self.search_button)

        # Wait for row to appear
        row_xpath = (
            By.XPATH,
            f"//div[@role='row'][.//div[text()='{username}']]"
        )

        row = self.wait.until(
            EC.visibility_of_element_located(row_xpath)
        )

        print("User found. Waiting 2 seconds before delete...")
        time.sleep(2)  

        # Delete only inside that row
        delete_button = row.find_element(
            By.XPATH,
            ".//button[.//i[contains(@class,'bi-trash')]]"
        )
        delete_button.click()

        # Confirm popup
        self.wait.until(
            EC.element_to_be_clickable(self.confirm_delete_btn)
        ).click()

        # Wait until row disappears
        self.wait.until(
            EC.invisibility_of_element_located(row_xpath)
        )

    # ---------------------------------------------------

    def reset_filter_with_refresh(self):

        self.driver.refresh()
        self.wait.until(
            EC.visibility_of_element_located(self.search_username_input)
        )
        search_box = self.wait.until(
            EC.visibility_of_element_located(self.search_username_input)
        )
        search_box.clear()
        self.click(self.search_button)
        self.wait.until(
            EC.text_to_be_present_in_element(self.records_label, "(")
        )