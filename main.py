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

rows = whs.row_count

whs.format("I2:I" + str(rows), {'numberFormat': {'type': 'CURRENCY', 'pattern': '€ #,###'}})

for i in range(2, rows):
    link = whs.acell(f'J{i}').value
    if link:
        page = requests.get(link).content
        soup = BeautifulSoup(page, "lxml")
        price = get_price(link, soup).strip()
        price = price.replace('€', '')
        price = price.replace(' ', '')
        current_price = whs.acell(f'I{i}').value
        if current_price != price:
            print(f'Updated price at cell I{i} from {current_price} to {price}')
            whs.update(f'I{i}', price)

whs.format("I2:I" + rows, {'type': 'CURRENCY', 'pattern': '€ #,###'})
