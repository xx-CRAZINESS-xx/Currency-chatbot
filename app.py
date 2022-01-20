from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
import httpx


app=Flask(__name__)

@app.route('/')

def index():
    return 'Hello'


@app.route('/',methods=['POST'])
def webhook():
    data=request.get_json()
    print(data)

    # to get corresponding values from json
    if data['queryResult']['parameters']['currency-name']=='':
        source=data['queryResult']['parameters']['unit-currency']['currency']
        amount=data['queryResult']['parameters']['unit-currency']['amount']
        target_currency='INR'

    elif data['queryResult']['parameters']['unit-currency']!='':
        source=data['queryResult']['parameters']['unit-currency']['currency']
        amount=data['queryResult']['parameters']['unit-currency']['amount']
        target_currency=data['queryResult']['parameters']['currency-name']

    else:
        source='INR'
        amount=1
        target_currency=data['queryResult']['parameters']['currency-name']

    print(source)
    print(amount)
    print(target_currency)

    convert_currency=fetch_convert_currency(source,target_currency)
    final_amount=amount*convert_currency
    response={
        'fulfillmentText':"{} {} is {} {}".format(amount,source,target_currency,final_amount,target_currency),
    }
    print(final_amount)
    return jsonify(response)


# function to scrap
def fetch_convert_currency(source, target_currency):
    url="https://www.google.com/search?q={}+{}".format(source,target_currency)
    response = httpx.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'})

    return float(data.text.split(' ')[0])
if __name__ == '__main__':
    app.run(debug=True)