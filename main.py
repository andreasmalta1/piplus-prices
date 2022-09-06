import gspread

sa = gspread.service_account(filename='service_account.json')
sh = sa.open('Pi Plus Price Sheet')

whs = sh.worksheet('Sheet1')

print('Rows:' , whs.row_count)
print('Columns:', whs.col_count)

# TODO: Read every link
# open link
# and edit price
# how I open link depends on domain name