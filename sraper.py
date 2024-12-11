import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

webdriver_path = r"C:\Users\MEGHA AIRAN\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

service = Service(webdriver_path)

driver = webdriver.Chrome(service=service)

try:
    driver.get("https://ci.policybazaar.com/v2/quotes?id=eWFjSk1kc1FsZFgvT3ljb1ZXQWZ1R1N5Z2M4b0YyRlRxKzZnQ3prWDIzUT0%3d&id2=L3dyVWJSbmcvL1hQQ0lkYTdVSElUQT09")
    
    driver.maximize_window()
    
    time.sleep(5)  
    
    plans = driver.find_elements(By.CLASS_NAME, "planCardWrap")  # Example class name; update accordingly
    
    # Prepare a list to hold scraped data
    scraped_data = []
    
    for plan in plans:
        try:
            # Extract the plan name
            plan_name = plan.find_element(By.CLASS_NAME, ".col.logo").text  # Update class name
            
            # Extract the plan price
            plan_price = plan.find_element(By.CLASS_NAME, "plan-price").text  # Update class name
            
            # Append the data as a dictionary
            scraped_data.append({
                "Price Name": plan_name,
                "Plan Price": plan_price
            })
        except Exception as inner_e:
            print(f"Error extracting data from a plan element: {inner_e}")
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_directory, "scraped_data3.csv")
    
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Price Name", "Plan Price"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for data in scraped_data:
            writer.writerow(data)
    
    print(f"Scraping completed. Data saved to {csv_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
