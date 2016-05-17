import urllib.request
import re
import schedule
import time
import getpass
import smtplib # Import smtplib for the actual sending function
from email.mime.text import MIMEText # Import the email modules we'll need


# To run this code, permission must be granted in GMAIL settings
print("Please allow apps to access gmail")

# Get password for demo purposes
password = getpass.getpass()

# List of Company ID's on Yahoo Finance and corresponding names
companies = ["aapl","goog","nflx"]
company_name = ["Apple","Google","Netflix"]

# Function that accesses stock value from Yahoo Finance and emails them daily
def get_stock_price(companies):
    outfile = open("stockprices.txt","w")
    # Erase previous text in email file
    emailfile = open("email.txt","w").close()
    emailfile = open("email.txt","w")
    i = 0
    while i < len(companies):
        # Use urllib library to access yahoo finance url for specific company ids
        url = "http://finance.yahoo.com/q?s="+companies[i]+"&q1=1"
        htmlfile = urllib.request.urlopen(url)
        htmltext = htmlfile.read()
        regex = '<span id="yfs_l84_' + companies[i] + '">(.+?)</span>'
        # Convert regex string to byte
        regex = regex.encode('utf-8')
        # Convert regular expression pattern into a regular expression object
        pattern = re.compile(regex)
        # Looks for the regex identifier in html code
        price = re.findall(pattern,htmltext)
        # Get the stock price for the company
        price = (price[0]).decode('utf-8')
        outfile.write(company_name[i]+' '+ price+' ')
        emailfile.write(company_name[i]+' '+ price+' ')
        print(price)
        i+=1
    outfile.close()
    emailfile.close()
    
    with open("email.txt") as fp:
        # Create a text/plain message
        msg = MIMEText(fp.read())
    msg['Subject'] = 'Daily Stock Prices'
    msg['From'] = "nriojas.60@gmail.com"
    msg['To'] = "me@nathanriojas.com"
    #s = smtplib.SMTP('localhost')
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.ehlo()
    s.starttls()
    # ENTER PASSWORD HERE or use getpass method
    s.login('nriojas.60@gmail.com', password)
    s.send_message(msg)
    s.quit()

    # url compiled at each company iteration
    # http://finance.yahoo.com/q?s=aapl&q1=1

# Use schedule library to run this function at a certain time each day
schedule.every().day.at("17:20").do(get_stock_price,companies)
print("running")
while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

# Note that this can be run easily in the backgroud on linux with
# the following command nohup python2.7 MyScheduledProgram.py &
