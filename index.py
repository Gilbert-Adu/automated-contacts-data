from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.firefox.options import Options # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time
import csv
import os
import re

#driver
firefox_options = Options()
firefox_options.add_argument("--headless")
#options=firefox_options
driver = webdriver.Firefox(options=firefox_options)

the_set = set()
driver_url = "https://www.publishersmarketplace.com/pm/search?ss_f_deal_region=&ss_f_contact_city=&ss_f_review_year=&ss_f_deal_category_key=&ss_f_contact_contact_category_key=&ss_f_review_month=&ss_f_deal_year=&ss_c=memberpage&ss_p_memberpage=5&ss_f_contact_state=&sub=Search&ss_q=fiction+AND+commercial&ss_f_dealmaker_dealmaker_type=&ss_f_deal_month="
data = []

def get_info():
    try:
        driver.get(driver_url)
        eq_mark = driver_url.index("=")
        and_mark = driver_url.index("&")
        members_list = driver.find_elements(By.XPATH, "//div[@class='DM-result Member-result']")
        search_val = driver_url[eq_mark+1:and_mark]
        for i in range(len(members_list)):
            details = members_list[i].text.splitlines()
            url = members_list[i].find_element(By.TAG_NAME, "a").get_attribute("href")
            name = details[0]
            company = details[1]
            role = details[2]
            if name.lower() not in the_set:
                if "agent" in role.lower() or "publisher" in role.lower() or "editor" in role.lower() or "editorial services" in role.lower() or "editor" in role.lower():
                    if "General Description" in details and details.index("General Description"):
                        general_description = details[details.index("General Description") + 1]
                    else:
                        general_description = ""
                        
                    if "Genres & Specialties" in details and details.index("Genres & Specialties"):
                        genres = details[details.index("Genres & Specialties") + 1]
                    else:
                        genres = ""

                    if "Key Personnel" in details or "Leading Clients" in details or "Best Known Projects" in details or "Special Experience" in details or "Recent Experience" in details:
                        
                        more = ""
                        if "Key Personnel" in details:
                            more += details[details.index("Key Personnel") + 1] + " "
                        if "Leading Clients" in details:
                            more += details[details.index("Leading Clients") + 1] + " "
                        if "Best Known Projects" in details:
                            more += details[details.index("Best Known Projects") + 1] + " "
                        if "Special Experience" in details:
                            more += details[details.index("Special Experience") + 1] + " "
                        if "Recent Experience" in details:
                            more += details[details.index("Recent Experience") + 1] + " "


                    else:
                        more = ""

                    


                    payload = {
                            "Name": name,
                            "Company": company,
                            "Role": role,
                            "Description": general_description,
                            "Genres_and_Specialties": genres,
                            "Further_Info": more,
                            "Keywords": search_val,
                            "URL": url,
                            
                    }
                    data.append(payload)

                    
                    the_set.add(name.lower())
            else:
                continue
        filename = "contacts.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            fieldnames = ["Name", "Company", "Role", "Description", "Genres_and_Specialties", "Further_Info", "Keywords", "URL"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            writer.writerows(data)
        print("finished inputting data in csv!")

    except Exception as e:

        print("This error occurred: ", str(e))




get_info()
time.sleep(5)

email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'  # Email regex
phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
website_pattern = r'(https?://[^\s]+)'  # Website URL regex
filename = 'contacts.csv'
try:
    # Read CSV
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Add new columns if not present
    if 'Email' not in fieldnames:
        fieldnames.append('Email')
    if 'Phone' not in fieldnames:
        fieldnames.append('Phone')
    if 'Website' not in fieldnames:
        fieldnames.append('Website')

    # Process each URL
    for row in rows:
        url = row['URL']  # URL from the 'contacts' column
        if url:
            try:
                # Load the web page
                driver.get(url)

                # Wait for the page to load fully
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Re-locate element to avoid stale reference
                page_text = driver.find_element(By.TAG_NAME, "body").text

                # Extract email, phone, and website using regex
                emails = re.findall(email_pattern, page_text)
                phones = re.findall(phone_pattern, page_text)
                websites = re.findall(website_pattern, page_text)

                # Update row
                row['Email'] = ', '.join(emails) if emails else ''
                row['Phone'] = ', '.join(phones) if phones else ''
                row['Website'] = ', '.join(websites) if websites else ''

            except Exception as e:
                print(f"Error processing {url}: {e}")
                row['Email'] = ''
                row['Phone'] = ''
                row['Website'] = ''

    # Write updated data back to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            # Keep only valid keys present in fieldnames
            filtered_row = {key: row[key] for key in fieldnames if key in row}
            writer.writerow(filtered_row)
        #writer.writerows(rows)

    print("CSV file updated with emails, phones, and websites.")

except Exception as e:
    print(f"An error occurred: {e}")


                    


"""
time.sleep(5)
                    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'  # Email regex
                    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                    website_pattern = r'(https?://[^\s]+)'  # Website URL regex
                    driver.get(url)
                    time.sleep(3)

                    # Wait for the page to load fully
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                    # Re-locate element to avoid stale reference
                    page_text = driver.find_element(By.TAG_NAME, "body").text

                    emails = re.findall(email_pattern, page_text)
                    phones = re.findall(phone_pattern, page_text)
                    websites = re.findall(website_pattern, page_text)

                    email_temp = ', '.join(emails) if emails else ''
                    phone_temp = ', '.join(phones) if phones else ''
                    website_temp = ', '.join(websites) if websites else ''



#---------------end--------
fiction and

--literary (this is probably the most important of these categories) done

--commercial - done

--confession

--erotic

--ethnic

--family saga

--historical

--metaphysical

--multicultural

--non-conventional

--edgy

--uncensored

--offbeat fiction

--narrative

--bio-fiction (or biographical fiction)

"""