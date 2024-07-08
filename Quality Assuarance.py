from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_current_data():
    driver = webdriver.Chrome()
    url = 'https://www.cars24.com/buy-used-car?f=make%3A%3D%3Atata&sort=bestmatch&serveWarrantyCount=true&storeCityId=2378'
    driver.get(url)
    time.sleep(5)  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    results = soup.find_all('div', {'class': '_2YB7p'})
    print(f'Total results found: {len(results)}')

    car_data = []
    for result in results:
        # Extracting car name - Adjusted based on actual site structure
        name_element = result.find('h3')  # Adjusted this based on the actual site structure
        name = name_element.get_text(strip=True) if name_element else 'N/A'

        # Extracting other details
        details = result.find('ul', {'class': '_3J2G-'}).find_all('li')
        kilometers = details[0].get_text(strip=True) if len(details) > 0 else 'N/A'
        year_of_manufacture = details[1].get_text(strip=True) if len(details) > 1 else 'N/A'
        fuel = details[2].get_text(strip=True) if len(details) > 2 else 'N/A'
        transmission = details[3].get_text(strip=True) if len(details) > 3 else 'N/A'

        price_element = result.find('strong', {'class': '_3RL-I'})
        price = price_element.get_text(strip=True) if price_element else 'N/A'

        emi_element = result.find('span', {'class': '_2O0yU'})
        emi = emi_element.get_text(strip=True) if emi_element else 'N/A'

        # Print extracted details 
        print(f'Name: {name}')
        print(f'Kilometers Driven: {kilometers}')
        print(f'Year of Manufacture: {year_of_manufacture}')
        print(f'Fuel: {fuel}')
        print(f'Transmission: {transmission}')
        print(f'Price: {price}')
        print(f'EMI: {emi}')
        print('---')

        car_data.append({
            'Name': name,
            'Year of Manufacturer': year_of_manufacture,
            'Distance Driven(in Km)': kilometers,
            'Fuel Type': fuel,
            'Transmission': transmission,
            'Price(in Lakhs)': price,
            'EMI (₹ / month)': emi
        })

    driver.quit()
    return car_data

# Load the CSV file into a DataFrame
csv_path = r"C:\Users\Ashmit\Desktop\Internship Project\Tata_Cars_Mumbai_CleanData.csv"
df_old = pd.read_csv(csv_path)

print("CSV File Loaded:")
print(df_old.head())  

# Scraping the current data from the Cars24 website
current_data = scrape_current_data()
df_new = pd.DataFrame(current_data)

print("Scraped Data:")
print(df_new.head())  

# Check columns and align DataFrames
print("CSV Columns:", df_old.columns)  
print("Scraped Data Columns:", df_new.columns)  


df_new = df_new[df_old.columns]  # This assumes columns in df_old and df_new match
df_old = df_old[df_old.columns]  # Ensure df_old columns are correct

# Set 'Name' as index for comparison
df_old.set_index('Name', inplace=True)
df_new.set_index('Name', inplace=True)

# Ensure both DataFrames have the same indexes
common_index = df_old.index.intersection(df_new.index)
df_old = df_old.loc[common_index]
df_new = df_new.loc[common_index]

# Checking if all values matches
comparison_result = df_old == df_new
mismatches = df_old[~comparison_result]

# Determine if all values matches
all_match = mismatches.empty

# Print DataFrames and comparison result
print("\nCSV Data (df_old):")
print(df_old)
print("\nScraped Data (df_new):")
print(df_new)
print("\nDiscrepancies (Unmatched Values):")
print(mismatches)
print("\nAll values match: ", all_match)
