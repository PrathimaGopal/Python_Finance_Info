from time import gmtime, strftime
import json
import requests
from flask import Flask,render_template,request
from yahoo_fin.stock_info import *

app = Flask(__name__)

def valid_ticker(ticker):
    #Check whether given ticker is a valid stock symbol.
    return get_name(ticker.upper()) != 'N/A'

@app.route('/', methods = ['GET'])
def index():
    if request.method == 'GET':
        return '''<title>Python Finance Info</title>
        <form method="POST">
            <h3>Python Finance Info</h3>
            <h6> Submitted by Prathima Gopal </h6><br>
            <i> Input: </i><br/><br/>
            Please enter a symbol: <br/> <input type="text" name="symbol"><br/><br/>
            <input type="submit" value="Submit"><br/><br/>
            </form>'''

@app.route('/', methods = ['POST'])
def result():
    if request.method == 'POST':
        #getting the Ticker Symbol from user
        tickerSymbol = request.form.get("symbol")
        tickerSymbol = tickerSymbol.upper()
        #Date and Time String
        date_string = strftime("%a %b %d %H:%M:%S PDT %Y", gmtime())
        #Connecting to Sandbox API to receive stock details

        try:
            url = "https://sandbox.iexapis.com/stable/stock/"+tickerSymbol+"/quote?token=Tpk_018b93ae93714677bc283c73c84cfa33"
            print("URL = "+url)
            result = requests.get(url)
            result.raise_for_status()

            reponseData = result.json()

            print("status code")
            print(result.status_code)

            if(result.status_code == 200):
                companyName = reponseData['companyName']
                valueChange = reponseData['change']
                percentChange = reponseData['changePercent']
                livePrice = get_live_price(tickerSymbol)

                #Formatting the variables
                livePrice = round(livePrice,2)
                valueChange = round(valueChange,2)
                if(valueChange > 0):
                    valueChange = "+" + str(valueChange)
                percentChange = percentChange*100
                percentChange = round(percentChange,2)
                if(percentChange >= 0):
                    percentChangeString = "(+" + str(percentChange) + "%)"
                else:
                    percentChangeString = "(" + str(percentChange) + "%)"

                #Formatting output strings
                print_companyName = "\n"+companyName+"  ("+tickerSymbol+")"
                print_rate = "\n"+str(livePrice)+"\t "+str(valueChange)+"\t "+str(percentChangeString)

        except:
            date_string = "You have entered incorrect ticker symbol!! Try with correct symbol."
            print_companyName, print_rate= " ", " "
   
       
        return '''<title>Python Finance Info</title>
        <form method="POST">
            <h3>Python Finance Info</h3>
            <h6> Submitted by Prathima Gopal </h6><br>
            <i> Input: </i><br/><br/>
            Please enter a symbol: <br/><input type="text" name="symbol"><br/><br/>
            <input type="submit" value="Submit"><br/><br/> 
            <i> Input: </i></br></br> Ticker symbol you entered: </br></br> {tickerSymbol} </br></br>
            <i> Output: </i>
            </br></br>{date_string}</br></br>{print_companyName}</br></br>{print_rate} </br></br>
        </form>'''.format(tickerSymbol= tickerSymbol, date_string= date_string, print_companyName=print_companyName, print_rate=print_rate)

@app.errorhandler(AttributeError)
def attribute_error_handle(e):
    return '''{}'''.format(e)

@app.errorhandler(ValueError)
def value_error_handle(e):
    return '''{}'''.format(e)

@app.errorhandler(404)
def page_not_found(e):
    return '''{}'''. format(e)

@app.errorhandler(500)
def internal_server_error(e):
    return '''{}'''. format(e)

if __name__ == '__main__':
    app.run(debug=True)