from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from form_filling_agent.config import FORM_URL
from form_filling_agent.prompts import name_prompt, email_prompt, phone_prompt, address_prompt
from form_filling_agent.utils import generate_response
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FormFillingAgent:
    def __init__(self, memory):
        self.memory = memory
        
        # Install ChromeDriver and set options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Maximize the window
        
        # Initialize the WebDriver with ChromeDriverManager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def fill_form(self):
        self.driver.get(FORM_URL)
        
        # Add a delay to ensure the page is fully loaded
        time.sleep(5)

        # Print the page source for debugging
        print(self.driver.page_source)
        
        # Fill the form fields using generated responses
        fields = {
            "name": name_prompt,
            "email": email_prompt,
            "phone": phone_prompt,
            "address": address_prompt
        }

        for field, prompt in fields.items():
            response = generate_response(prompt)
            self.memory.update(field, response)
            
            try:
                # Wait until the element is present
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, field))
                )
                element.send_keys(response)
            except Exception as e:
                print(f"Exception occurred while locating element {field}: {e}")
        
        try:
            # Upload the resume (assuming the resume file path is stored in memory)
            resume_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "fileUpload"))
            )
            resume_element.send_keys(self.memory.data.get("resume_path"))

            # Submit the form
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "input_2"))
            )
            submit_button.click()
        except Exception as e:
            print(f"Exception occurred while uploading resume or submitting the form: {e}")
    
    def quit(self):
        self.driver.quit()
