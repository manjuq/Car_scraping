# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup

# %%
url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=mercedes_benz&maximum_distance=20&models[]=&page=1&stock_type=cpo&zip='
# Making an HTTP GET request to the URL
page = requests.get(url)
# Parsing the page content using BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

# %%
alls = []
# Finding elements based on criteria (e.g., tag, class)
results = soup.find_all('div', attrs={'class': 'vehicle-card'})
for result in  results:
    all1 = []

# Finding the first element that matches criteria
    name = result.find('a', {'class':'vehicle-card-link'})
    mileage = result.find('div', {'class': 'mileage'})
    price = result.find('span', {'class': 'primary-price'})
    rating = result.find('span', {'class':'sds-rating__count'})
    rate_count = result.find('span', {'class': 'sds-rating__link sds-button-link'})
    car_dealer_name = result.find('div', {'class': 'dealer-name'})

    if name is not None:
        all1.append(name.find('h2').text)
    else:
# Adding extracted data to a list
        name.append('na')
    
    if mileage is not None:
        all1.append(mileage.text)
    else:
        mileage.append('na')
    
    if price is not None:
        all1.append(price.text)
    else:
        price.append('na')
    
    if rating is not None:
        all1.append(rating.text)
    else:
        all1.append('na')

    if rate_count is not None:
        all1.append(rate_count.text)
    else:
        rate_count.append('na')

    if car_dealer_name is not None:
        all1.append(car_dealer_name.text.strip())
    else:
        all1.append('na')
 
# Adding the car's data to the main list
    alls.append(all1)


# %%
# Converting the list of data into a pandas DataFrame
df = pd.DataFrame(alls, columns=['Name', 'Mileage', 'Price', 'Rating', 'Rate Count', 'Dealer Name'])
df

# %% [markdown]
# Data Cleaning

# %%
df['Rate Count'] = df['Rate Count'].apply(lambda x: x.strip('reviews)').strip('('))

# %% [markdown]
# Stroing output in Excel

# %%
df.to_excel('single_page_car.xlsx', index=False)

# %% [markdown]
# Part-2 Pagination

# %%
name = []
mileage = []
dealer_name = []
rating = []
rating_count = []
price = []

for i in range(1,11):   

    #website in a variable
    website = f'https://www.cars.com/shopping/results/?list_price_max=&makes[]=mercedes_benz&maximum_distance=20&models[]=&page={i}&stock_type=cpo&zip='

    #request to a website
# Making an HTTP GET request to the URL
    response = requests.get(website)

    #soup object
# Parsing the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    #results 
# Finding elements based on criteria (e.g., tag, class)
    results = soup.find_all('div', {'class': 'vehicle-card'})

    
    for result in  results:

        #name
        try:
            name.append(result.find('h2').get_text())
        except:
            name.append('na')

        #mileage
        try:
            mileage.append(result.find('div', {'class': 'mileage'}).get_text())
        except:
            mileage.append('na')

        #dealer name
        try:
            dealer_name.append(result.find('div', {'class': 'dealer-name'}).get_text().strip())
        except:
            dealer_name.append('na')

        #rating
        try:
            rating.append(result.find('span', {'class':'sds-rating__count'}).get_text())
        except:
            rating.append('na')
        
        #rate count
        try:
            rating_count.append(result.find('span', {'class': 'sds-rating__link sds-button-link'}).get_text())
        except:
            rating_count.append('na')

        #price
        try:
            price.append(result.find('span', {'class': 'primary-price'}).get_text())
        except:
            price.append('na')
            

# %%
# Converting the list of data into a pandas DataFrame
car_dealer = pd.DataFrame({'Name':name, 'Mileage':mileage, 'Dealer_name':dealer_name,
                                'Rating':rating, 'Rating_count': rating_count, 'Price':price})

# %%
car_dealer['Rating_count'] = car_dealer['Rating_count'].apply(lambda x:x.strip('reviews)').strip('('))

# %%
car_dealer.to_excel('multiple_pages_car.xlsx', index=False)


