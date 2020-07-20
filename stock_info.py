#author: David Edwards
#Date:   July 16 2020

#import python requests module to make api calls
import requests
import json
import smtplib
import pprint
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from collections import OrderedDict 

#defining api endpoint
url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

#headers containing api key for authentication purposes
headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "#########################################"
}
i=0
total_body = OrderedDict()
def main():
    #defining arguments, region, language and stock symbols
    symbols = {0:"AAPL", 1:"KXS.TO"}
    for sym in symbols:
        querystring = {"symbol": str(symbols[sym])}
        call_api(querystring)
    sendalert()

def call_api(querystring):
    #actual http GET request to retrieve stock information and store into json object
   
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code!=200:
        raise Exception('Radapi call failed, exiting program')
        sys.exit()
    #convert json object into python nested dict
    else:
        dict_response = json.loads(response.text)
        global i, total_body,body
        #break nested dict
        market_data= dict_response["summaryDetail"]
        sym= str(dict_response["symbol"])
        current_price = (float)dict_response["price"]["regularMarketPrice"]["raw"]
        prev_price = (float)dict_response["price"]["regularMarketPreviousClose"]["raw"]
        fifty_high = (float)market_data["fiftyTwoWeekHigh"]["raw"]
        fifty_mov= (float)market_data["fiftyDayAverage"]["raw"]
        two_hund_mov= (float)market_data["twoHundredDayAverage"]["raw"]
        #evaluate trade status using data pulled from api call
        if (fifty_high - current_price < 2.0):
            status = "Strong Buy"
        elif(fifty_mov>two_hund_mov and current_price>fifty_mov):
            status = "Buy|Hold"
        elif(current_price-prev_price < (-2.0)
            status = "Possible Sell, monitor"
        else:
            status = "Sell"

        #storing data in ordered dictionary to preserve order of key/value insertion
        body = OrderedDict([("Symbol",sym), ("Market price",current_price, ("Fifty Moving Average",fifty_mov), ("Two Hundred Moving Average", two_hund_mov), ("Fifty Two Week High", fifty_high ), ("Quantitative Trade Status", status )])
        body = {i: body  }
        total_body.update(body)
        i+=1
    
def sendalert():
    global total_body
    from_address = "email"
    to_address = "testemail
    subject= "Stock Update " + str(datetime.now())
    
    # Credentials and message
    username = 'email'  
    password = '#########################################' 
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    total_body= json.dumps(total_body, indent=2)
    msg.attach(MIMEText(total_body,'plain'))
    email_text = msg.as_string()
    
    
    #establishing tls encription to send email to smtp server
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    server.login(username,password)  
    server.sendmail(from_address, to_address, email_text)  
    server.quit()


if __name__ == "__main__":
    main()