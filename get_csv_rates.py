import time
from datetime import datetime as date
from datetime import timedelta
from selenium import webdriver

def convert_month(month):
    # convert month text to number
    list_month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep', 'oct','Nov','Dec']
    return list_month.index(month)+1

def set_date():
    # set date of today and before ten days

    # set dates
    today = date.today()
    ten_days_ago = today - timedelta(days=10)

    # convert by timestamp
    today = str(time.mktime(today.timetuple()))
    ten_days_ago = str(time.mktime(ten_days_ago.timetuple()))

    # adjust the thimestamp
    today = today[:len(today)-2]
    ten_days_ago = ten_days_ago[:len(ten_days_ago)-2]

    return [today,ten_days_ago]

def generate_csv():
    global driver
    # set header
    csv = "Date,BTC Closing Value\n"
    # loop for add one more line in csv
    for i in range(10):
        # set column 1
        path = ('//*[@id="Col1-1-HistoricalDataTable-Proxy"]'+
        '/section/div[2]/table/tbody/tr['+str(1+i)+']/td[1]/span')
        el = driver.find_element('xpath',path).get_attribute('innerText')
        el = el.split(' ')
        el[0] = convert_month(el[0])
        el[1] = el[1][:len(el[1])-1]
        el = str(el[1]) + '-' + str(el[0]) + '-' + str(el[2])
        csv += el +","

        # set column 2
        try:
            path = ('//*[@id="Col1-1-HistoricalDataTable-Proxy"]'+
            '/section/div[2]/table/tbody/tr['+str(1+i)+']/td[5]/span')
            el = driver.find_element('xpath',path).get_attribute('innerText')
            el = el.split(',')
            el = str(el[0]) + str(el[1])
            csv += el +"\n"
        except:
            print('Element by number ['+str(i)+'] no find')
            csv += " - \n"
    return csv

def generate_file(value):
    # generate csv file
    t = date.today()
    t = str(t.year) + '_' + str(t.month) + '_' + str(t.day)
    file = open('./eur_btc_rates_' + t + '.csv', 'w+')
    file.write(value)
    file.close()

# ---

today , ten_days_ago = set_date()

# set url
url = ('https://finance.yahoo.com/quote/BTC-EUR/history?'+
'period1='+ten_days_ago+'&'+
'period2='+today+'&'+
'interval='+'1d'+'&'
'filter='+'history'+'&'
'frequency='+'1d'+'&'
'includeAdjustedClose='+'true')

# ---

# start driver
op = webdriver.ChromeOptions()
op.binary_location = '/usr/bin/brave-browser-stable'
driver = webdriver.Chrome('/usr/bin/chromedriver',9515,op)
print("\n")

# ---

driver.get(url)
csv = generate_csv()
driver.close()
generate_file(csv)

print('Successfully generated!')
