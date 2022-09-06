import gspread
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

def get_price(url, soup):
    domain = urlparse(url).netloc

    if 'scan' in domain:
        return soup.find('span', class_='price').get_text()
    
    if 'klikk' in domain:
        return soup.find('p', class_='product_detail_price').get_text()
    
    if 'rs' in domain:
        rs_price = soup.find_all('p', class_='add-to-basket-cta-component_unit-price__1g5u8')
        return rs_price[1].get_text()
        
    if 'atoz' in domain:
        az_price = soup.find('div', class_='product_productprice').get_text()
        az_price = az_price.replace('AtoZ Promotion ', '')
        return az_price.replace(' Inc VAT', '')

sa = gspread.service_account(filename='service_account.json')
sh = sa.open('Pi Plus Price Sheet')

whs = sh.worksheet('Sheet1')

url = whs.acell('J2').value
# val = worksheet.cell(1, 2).value
# values_list = worksheet.row_values(1)

page = requests.get(url).content
soup = BeautifulSoup(page, "lxml")

price = get_price(url, soup)

whs.update('I2', price)

print(price)

# Make it dyanmaic

