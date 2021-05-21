import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3
car_name = []
year = []
price=[]
car_type=[]
kms = []
for i in range(1,6):
    web = requests.get('https://www.cars24.com/buy-used-cars-pune/?itm_source=Cars24Website&itm_medium=sticky_header&page='+str(i))
    html_code = bs(web.content,'html.parser')
    div = html_code.find_all('div',attrs={'class':'_3ENhq'})
    for i in div:
        c = i.string
        y = re.findall(r'\A[0-9]*',c)
        c = c.replace(*y,'')
        car_name.append(c)
        year.append(*y)
    p = html_code.find_all('h3',attrs={'class':'_6KkG6'})
    for i in p:
        price.append(i.get_text())
    s = html_code.find_all('span',attrs={'itemprop':'name'})
    for i in s:
        car_type.append(i.string)
    u = html_code.find_all('div',attrs={'class':'_Ecri'})
    for i in u:
        u1 = i.find('span')
        kms.append(u1.get_text())
try:
    try:
        print('connecting....')
        conn = sqlite3.connect('cars_data.db')
        print('connected')
    except:
        print('can not connect..')
    cursor = conn.cursor()
    try:
        print('creating table...')
        cursor.execute('CREATE TABLE IF NOT EXISTS Cars(Car_Name TEXT, Year TEXT, price TEXT, Type TEXT, Used TEXT)')
        print('table created.')
    except:
        print('table already craeted.')
    try:
        print('Inserting Data.....')  
        for i in range(len(car_name)):
            cursor.execute('INSERT INTO Cars(Car_Name,Year,price,Type,Used) VALUES(?,?,?,?,?)',(car_name[i],year[i],price[i],car_type[i],kms[i]))
        conn.commit()
        print('Data inserted.')
    except:
        print("Invalid Table")
    print('Success..')
    
except:
    print('Failed...')