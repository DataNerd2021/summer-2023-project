import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandasql import sqldf
import warnings
warnings.filterwarnings('ignore')

# read input csv
vins = pd.read_csv('vins.csv')

# read output csv
features = pd.read_csv('unclean_output.csv')

# clean output "vin" field
features['vin'] = 'VIN' + features['vin']

# do an anti-join to eliminate duplicate records
vins2 = sqldf('SELECT DISTINCT vin FROM vins WHERE vin NOT IN(SELECT DISTINCT vin FROM features)')
def scrape_listings(page_num, max_page_num):
    while page_num <= max_page_num:
        
        # define url to scrape

        url= f'https://www.truecar.com/used-cars-for-sale/listings/?page={page_num}'

        # confirm HTTP response
        
        response = requests.get(url, timeout=10)
            
        # define parser variable
        
        soup = BeautifulSoup(response.content, 'html.parser')

        results = soup.find_all('div', {'class' : 'linkable card card-shadow vehicle-card'})
        
        # get individual attributes and append to List
        
        vin = []
        header = []
        trim = []
        price = []

        for result in results:
    
            # vin
            try:
                vin.append(result.find('div', {'class':'vehicle-card-vin-carousel mt-1 text-xs'}).get_text())
            except:
                break
            
            try:
                header.append(result.find('div', {'class': 'vehicle-card-header w-full'}).get_text())
            except:
                break
            
            try:
                trim.append(result.find('div', {'class': 'truncate text-xs'}).get_text())
            except:
                break
            
            try:
                price.append(result.find('div', {'data-test':'vehicleCardPricingBlockPrice'}).get_text())
            except:
                break
        try:
            car_listings = pd.DataFrame({'page_num':page_num, 'vin': vin, 'header':header, 'trim':trim, 'price':price})
                
            car_listings.to_csv('vins.csv', index=False, mode='a', header=False)
            print(f'Page {page_num} scraped and loaded')
            page_num += 1
        except ValueError:
            print(f'Page {page_num} Error. Continue Loop')
            page_num += 1

def scrape_features(row_num, max_row_num):
    # read input csv
    df = pd.read_csv('vins.csv', low_memory=False)
    
    # read output csv
    df2 = pd.read_csv('unclean_output.csv', low_memory=False)
    
    # clean output csv
    df2['vin'] = 'VIN' + df2['vin']
    
    # set minimum and maximum page values
    max_page_num = sqldf('SELECT MAX(page_num) FROM df')
    min_page_num = sqldf('SELECT MIN(page_num) FROM df')
    max_page_num = max_page_num.iloc[0]['MAX(page_num)']
    min_page_num = min_page_num.iloc[0]['MIN(page_num)']
    
    # conduct anti-join to eliminate duplicate records
    df = sqldf(f"SELECT DISTINCT vin, header, trim, price FROM df WHERE vin NOT IN(SELECT DISTINCT vin FROM df2) AND page_num BETWEEN {min_page_num} AND {max_page_num}")
    
    # clean temp input "vin" field
    df['vin'] = df['vin'].str.replace('VIN', '')
    
    # reshape the dataset
    df = df.reset_index()
    
    # iterate over remaining records
    while row_num < max_row_num:
        # set independent variabe values
        vin = df['vin'][row_num]
        header = df['header'][row_num]
        trim = df['trim'][row_num]
        price = df['price'][row_num]
        
        # define url to scrape
        url = f'https://truecar.com/used-cars-for-sale/listing/{vin}/'

        # confirm HTTP response
        response = requests.get(url, timeout=15)

        # define HTML parser variable
        soup = BeautifulSoup(response.content, 'html.parser')

        if response.status_code == 200:
            results = soup.find_all('div', {'class':'mb-3 lg:mb-4 col-12 col-lg-6'})

            # Iterate through individual data point and append to temp list
            data = []
            try:
                for result in results:
                    data.append(result.find('h3', {'class':'heading-base flex items-center'}).get_text())
                data = pd.DataFrame({'vin':vin, 'header':header, 'trim':trim, 'price':price, 'location':data[0], 'mileage':data[1], 'exterior_color':data[2], 'interior_color':data[3], 'fuel_type':data[4], 'mpg':data[5], 'transmission':data[6], 'drivetrain':data[7], 'engine':data[8]}, index=[0])
                data.to_csv('unclean_output.csv', index=False, header=False, mode='a')
                print(f'Listings Completed: {row_num}/{len(df)}')
                row_num += 1
                
            # if the MPG field is missing on the page, exclude it from the list
            except:
                try:
                    for result in results:
                        data.append(result.find('h3', {'class':'heading-base flex items-center'}).get_text())
                    data = pd.DataFrame({'vin':vin, 'header':header, 'trim':trim, 'price':price, 'location':data[0], 'mileage':data[1], 'exterior_color':data[2], 'interior_color':data[3], 'fuel_type':data[4], 'mpg':'N/A', 'transmission':data[5], 'drivetrain':data[6], 'engine':data[7]}, index=[0])
                    data.to_csv('unclean_output.csv', index=False, header=False, mode='a')
                    print(f'Listings Completed: {row_num}/{len(df)}')
                    row_num += 1
                
                # if the list is empty, print the following string    
                except:
                    print(f'{vin}: {data}')
                    row_num += 1

#scrape_listings(100,201)
#time.sleep(3.0)
while len(vins2) >= 0:
    scrape_features(0,len(vins2))