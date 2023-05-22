import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random

def scrape_listings():
    page_num = 1
    while page_num <= 50:
        cities = ['salt-lake-city-ut', 'oklahoma-city-ok', 'seattle-wa', 'denver-co', 'austin-tx', 'boston-ma', 'orlando-fl', 'buffalo-ny', 'milwaukee-wi', 'chicago-il', 'boise-id', 'fargo-nd', 'bismarck-nd', 'phoenix-az', 'los-angeles-ca', 'reno-nv', 'santa-fe-nm', 'witchita-ks', 'new-orleans-la', 'little-rock-ar', 'atlanta-ga', 'billings-mt', 'detroit-mi', 'sacramento-ca', 'st-louis-mo', 'cheyenne-wy', 'augusta-me', 'richmond-va', 'lincoln-ne', 'charleston-sc', 'portland-or', 'provo-ut', 'new-york-ny', 'spokane-wa', 'indianapolis-in', 'flagstaff-az', 'sioux-falls-sd', 'springfield-mo', 'carson-city-nv', 'charlottesville-va', 'el-paso-tx']
        url= f'https://www.truecar.com/used-cars-for-sale/listings/location-{random.choice(cities)}/?excludeExpandedDelivery=true&page={page_num}&searchRadius=500'

        response = requests.get(url, timeout=10)

        response.status_code
        
        soup = BeautifulSoup(response.content, 'html.parser')

        results = soup.find_all('div', {'class' : 'linkable card card-shadow vehicle-card'})
        
        vin = []
        header = []
        trim = []
        price = []
        mileage = []
        colors = []
        condition = []
        location = []

        for result in results:
    
            # vin
            try:
                vin.append(result.find('div', {'class':'vehicle-card-vin-carousel mt-1 text-xs'}).get_text())
            except:
                exit
            # header
            try:
                header.append(result.find('div', {'class':'vehicle-card-header'}).get_text())
            except:
                header.append('n/a')
            
            # trim
            try:
                trim.append(result.find('div', {'data-test':'vehicleCardTrim'}).get_text())
            except:
                trim.append('n/a')
            # price
            try:
                price.append(result.find('div', {'class':'vehicle-card-bottom-pricing-secondary pl-3 lg:pl-2 vehicle-card-bottom-max-50'}).get_text())
            except:
                exit
            
            # mileage
            try:
                mileage.append(result.find('div', {'data-test':'vehicleMileage'}).get_text())
            except:
                mileage.append('n/a')
            
            # colors
            try:
                colors.append(result.find('div', {'data-test':'vehicleCardColors'}).get_text())
            except:
                colors.append('n/a')
            
            # condition
            try:
                condition.append(result.find('div', {'data-test':'vehicleCardCondition'}).get_text())
            except:
                condition.append('n/a')
            
            # location
            try:
                location.append(result.find('div', {'data-test': 'vehicleCardLocation'}).get_text())
            except:
                location.append('n/a')
        

        car_listings = pd.DataFrame({'vin': vin, 'header': header, 'trim': trim, 'price': price, 'mileage': mileage, 'colors': colors, 'condition': condition, 'location': location})
        
        # extract model year from listing header  
        
        car_listings['year'] = np.where(car_listings['header'].str.startswith('Spon'), car_listings['header'].str[9:13], car_listings['header'].str[:5])
        
        # extract make and model from listing header
        
        try:
            new_cols = car_listings['header'].str.split(" ", n=5, expand=True)
            car_listings['make'] = new_cols[1]
            car_listings['model'] = new_cols[2]
            car_listings['model2'] = new_cols[3]
            car_listings['model3'] = new_cols[4]
        except KeyError:
            try:
                new_cols = car_listings['header'].str.split(" ", n=4, expand=True)
                car_listings['make'] = new_cols[1]
                car_listings['model'] = new_cols[2]
                car_listings['model2'] = new_cols[3]
            except:
                new_cols = car_listings['header'].str.split(" ", n=3, expand=True)
                car_listings['make'] = new_cols[1]
                car_listings['model'] = new_cols[2]

            
        # drop header column and reorder columns
            
        car_listings = car_listings.drop(columns=['header'])
        try:
            car_listings = car_listings[['vin', 'year', 'make', 'model', 'model2', 'model3', 'trim', 'price', 'mileage', 'colors', 'condition', 'location']]
        except:
            try:
                car_listings = car_listings[['vin', 'year', 'make', 'model', 'model2', 'trim', 'price', 'mileage', 'colors', 'condition', 'location']]
            except:
                car_listings = car_listings[['vin', 'year', 'make', 'model', 'trim', 'price', 'mileage', 'colors', 'condition', 'location']]
            
        # clean price column and convert to int    
        
        car_listings['price'] = car_listings['price'].str.replace('$', '')
        car_listings['price'] = car_listings['price'].str.replace(',', '')
        try:
            car_listings['price'] = car_listings['price'].astype(int)
        except:
            car_listings['price'] = np.nan
            
        # clean mileage column and convert to int    
        
        car_listings['mileage'] = car_listings['mileage'].str.replace('miles', '')
        car_listings['mileage'] = car_listings['mileage'].str.replace(',', '')
        car_listings['mileage'] = car_listings['mileage'].astype(int)
        
        # split colors column into exterior_color and interior_color columns
        
        new_cols = car_listings['colors'].str.split(",", n=2, expand=True)
        car_listings['exterior_color'] = new_cols[0]
        car_listings['interior_color'] = new_cols[1]
        
        # clean exterior_color and interior_color columns
        
        car_listings['exterior_color'] = car_listings['exterior_color'].str.replace('exterior', '')
        car_listings['interior_color'] = car_listings['interior_color'].str.replace('interior', '')
        
        # clean location column
        
        car_listings['location'] = car_listings['location'].str.replace('Online RetailerDelivery Available', 'Online')
        
        # drop colors column and split condition column
        
        car_listings = car_listings.drop(columns=['colors'])

        new_cols = car_listings['condition'].str.split(", ", n=3, expand=True)
        car_listings['num_accidents'] = new_cols[0]
        car_listings['num_owners'] = new_cols[1]
        car_listings['use_type'] = new_cols[2]
        
        # drop condition column and clean num_accidents, num_owners, and use_type columns
        
        car_listings = car_listings.drop(columns=['condition'])

        car_listings['num_accidents'] = np.where(car_listings['num_accidents'].str.contains('No'), '0', car_listings['num_accidents'].str[0:1])
        car_listings['num_accidents'] = car_listings['num_accidents'].str.strip()
        car_listings['num_owners'] = car_listings['num_owners'].str[0:1]
        car_listings['num_owners'] = car_listings['num_owners'].str.strip()
        car_listings['use_type'] = car_listings['use_type'].str.replace('use', '')
        
        # convert num_accidents to int and use_type to categorical
        
        car_listings['num_accidents'] = car_listings['num_accidents'].astype(int)
        try:
            car_listings['num_owners'] = car_listings['num_owners'].astype(int)
        except:
            car_listings['num_owners'] = car_listings['num_owners'].str.replace('p','')
            car_listings['num_owners'] = car_listings['num_owners'].str.replace('P','')
            car_listings['num_owners'] = car_listings['num_accidents'].str.strip()
            car_listings['num_owners'] = car_listings['num_owners'].astype(int)
        car_listings['use_type'] = car_listings['use_type'].astype('category')
        
        # split location column
        
        new_cols = car_listings['location'].str.split(", ", n=2, expand=True)
        car_listings['city'] = new_cols[0]
        car_listings['state'] = new_cols[1]
        
        # clean city column
        
        car_listings['city'] = np.where(car_listings['city'].str.contains('mi -'), car_listings['city'].str.replace('mi -', ''), car_listings['city'])
        
        # drop location column and reorder columns
        
        car_listings = car_listings.drop(columns=['location'])

        try:
            car_listings = car_listings[['vin', 'year', 'make', 'model', 'model2', 'model3', 'trim', 'price', 'mileage', 'city', 'state', 'exterior_color', 'interior_color', 'num_accidents', 'num_owners', 'use_type']]
        except:
            try:
                car_listings = car_listings[['vin', 'year', 'make', 'model', 'model2', 'trim', 'price', 'mileage', 'city', 'state', 'exterior_color', 'interior_color', 'num_accidents', 'num_owners', 'use_type']]
            except:
                car_listings = car_listings[['vin', 'year', 'make', 'model', 'trim', 'price', 'mileage', 'city', 'state', 'exterior_color', 'interior_color', 'num_accidents', 'num_owners', 'use_type']]
            
        # fill in drivetrain column    
            
        car_listings['drivetrain'] = np.where(car_listings['trim'].str.contains('FWD'), 'FWD', np.where(car_listings['trim'].str.contains('RWD') | car_listings['trim'].str.contains('2WD'), 'RWD', np.where(car_listings['trim'].str.contains('4WD'), '4WD', np.where(car_listings['trim'].str.contains('AWD'), 'AWD', 'Unknown'))))
        
        # concatenate model columns
        
        try:
            car_listings['model2'] = car_listings['model2'].fillna('')
            car_listings['model3'] = car_listings['model3'].fillna('')
            car_listings['model'] = np.where(car_listings['model3'] != None, car_listings['model'] + " " + car_listings['model2'] + " " + car_listings['model3'], np.where(car_listings['model2'] != None, car_listings['model'] + " " + car_listings['model2'], car_listings['model']))
        except:
            try:
                car_listings['model2'] = car_listings['model2'].fillna('')
                car_listings['model'] = np.where(car_listings['model2'] != None, car_listings['model'] + " " + car_listings['model2'], car_listings['model'])
            except:
                car_listings['model'] = car_listings['model']
        
        # drop model2 and model3 columns and fill in transmission column
        
        try:
            car_listings = car_listings.drop(columns=['model2', 'model3'])
        except:
            car_listings = car_listings.drop(columns=['model2'])

        car_listings['transmission'] = np.where(car_listings['trim'].str.contains('CVT'), 'CVT', np.where(car_listings['trim'].str.contains('Automatic'), 'Automatic', 'Unknown'))
        
        # clean trim column and reorder columns
        
        car_listings['trim'] = car_listings['trim'].str.replace('4WD', '')
        car_listings['trim'] = car_listings['trim'].str.replace('AWD', '')
        car_listings['trim'] = car_listings['trim'].str.replace('FWD', '')
        car_listings['trim'] = car_listings['trim'].str.replace('RWD', '')
        car_listings['trim'] = car_listings['trim'].str.replace('2WD', '')
        car_listings['trim'] = car_listings['trim'].str.replace('CVT', '')
        car_listings['trim'] = car_listings['trim'].str.replace('Automatic', '')

        car_listings = car_listings[['vin', 'year', 'make', 'model', 'trim', 'price', 'mileage', 'drivetrain', 'transmission', 'city', 'state', 'exterior_color', 'interior_color', 'num_accidents', 'num_owners', 'use_type']]
        
        # set official data types
        
        car_listings['year'] = car_listings['year'].str.strip()
        car_listings['year'] = car_listings['year'].astype(int)

        car_listings['drivetrain'] = car_listings['drivetrain'].astype('category')

        car_listings['transmission'] = car_listings['transmission'].astype('category')
        
        # clean city column
        
        all_listings1 = pd.read_csv('car_listings2.csv', low_memory=False)
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        all_listings1['city'] = all_listings1['city'].str.replace('.', '')
        all_listings1['city'] = all_listings1['city'].str.strip()
        for i in digits:
            all_listings1['city'] = all_listings1['city'].str.replace(i, '')
        all_listings1['city'] = all_listings1['city'].str.replace('mi -', '')
        all_listings1['city'] = np.where(all_listings1['city'].str.contains('Online'), 'Online', all_listings1['city'])
            
        all_listings1 = pd.read_csv('car_listings2.csv', low_memory=False)
        outer = car_listings.merge(all_listings1, how='outer', indicator=True)
        anti_join = outer[(outer._merge=='left_only')].drop('_merge', axis=1)
        anti_join.to_csv('car_listings2.csv', index=False, mode='a', header=False)
        print(f'Page {page_num} scraped and loaded from {url[52:80]}')
        page_num += 1

i = 0
while i <= 10:
    scrape_listings()
    print(f'Batch {i} completed')
    i += 1