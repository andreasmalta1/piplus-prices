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
range_links = f'J2:J{rows}'
range_prices = f'I2:I{rows}'

list_links = whs.get(range_links)
list_prices = []

for link in list_links:
    if not link:
        list_prices.append(['NA'])
    else:
        link = link[0]
        page = requests.get(link).content
        soup = BeautifulSoup(page, "lxml")
        price = get_price(link, soup).strip()
        price = price.replace('€', '')
        price = price.replace(' ', '')
        list_prices.append([price])

# 48 = NA
# 96 = 1054
whs.update('I2:I96', list_prices)
# worksheet.format('A1:B1', {'textFormat': {'bold': True}})
# worksheet.format("A2:B2", {
#     "backgroundColor": {
#       "red": 0.0,
#       "green": 0.0,
#       "blue": 0.0
#     },
#     "horizontalAlignment": "CENTER",
#     "textFormat": {
#       "foregroundColor": {
#         "red": 1.0,
#         "green": 1.0,
#         "blue": 1.0
#       },
#       "fontSize": 12,
#       "bold": True
#     }
# })

# try manually for 2 rows
# formatting
# https://docs.gspread.org/en/latest/user-guide.html
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#cellformat
# https://github.com/robin900/gspread-formatting