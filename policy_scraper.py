import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

webdriver_path = r""
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service)

try:
    # Open the target webpage
    driver.get("https://ci.policybazaar.com/v2/quotes?id=eWFjSk1kc1FsZFgvT3ljb1ZXQWZ1R1N5Z2M4b0YyRlRxKzZnQ3prWDIzUT0%3d&id2=L3dyVWJSbmcvL1hQQ0lkYTdVSElUQT09")
    
    # Maximize the browser window
    driver.maximize_window()

    # Wait for the page to load completely
    time.sleep(5)

    # Locate all plan cards
    plans = driver.find_elements(By.CLASS_NAME, "planCardWrap")  # Update class name accordingly

    # Prepare a list to hold scraped data
    scraped_data = []

    # Loop through each plan card and extract the details
    for plan in plans:
        try:
            # Extract the company logo and name
            logo = plan.find_element(By.CSS_SELECTOR, ".logo img")
            company_name = logo.get_attribute("alt")
            logo_url = logo.get_attribute("src")
            
            # Extract IDV cover
            idv_cover = plan.find_element(By.CSS_SELECTOR, ".idv .headingV3.fontNormal").text
            
            # Extract Claims Settled
            claims_settled = plan.find_element(By.CSS_SELECTOR, ".claim .headingV3.fontNormal").text
            
            # Extract plan price
            plan_price = plan.find_element(By.CSS_SELECTOR, ".planBtn .btnContent").text.split("₹")[1].strip()

            # Extract features
            features = plan.find_elements(By.CSS_SELECTOR, ".featureItem p.smallerFont")
            features_text = [feature.text for feature in features]

            # Append the data as a dictionary
            scraped_data.append({
                "Company Name": company_name,
                "Logo URL": logo_url,
                "IDV Cover": idv_cover,
                "Claims Settled": claims_settled,
                "Plan Price": plan_price,
                "Features": ", ".join(features_text)  # Join multiple features into a single string
            })
        except Exception as inner_e:
            print(f"Error extracting data from a plan element: {inner_e}")

    # Prepare file path to save the data
    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_directory, "scraped_data_new.csv")
    
    # Write data to CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Company Name", "Logo URL", "IDV Cover", "Claims Settled", "Plan Price", "Features"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for data in scraped_data:
            writer.writerow(data)
    
    print(f"Scraping completed. Data saved to {csv_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
