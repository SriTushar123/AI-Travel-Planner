import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json

class CurrencyExchanger():
    def __init__(self):
        self.base_url = f"https://v6.exchangerate-api.com/v6/{os.getenv('CURRENCY_EXCHANGE_API')}/latest"

    def currency_exchanger(self,from_currency:str,to_currency:str,amount:float):
        url = f"{self.base_url}/{from_currency}"
        response = requests.get(url)
        if(response.status_code!=200):
            raise Exception("API call failed")
        rate = response.json()["conversion_rates"]
        if (to_currency not in rate):
            raise Exception(f"{to_currency} not present")
        # final_amount = rate[to_currency]*amount
        final ={
            "Status":response.json()["result"],
            "data": {
                "from_currency":from_currency,
                "to_currency":to_currency,
                "conversion_rate":response.json()["conversion_rates"][to_currency],
                "amount_by_user":f"{amount} {from_currency}",
                "final_amount_after_conversion":f"{response.json()['conversion_rates'][to_currency]*amount} {to_currency}"
            }
        }
        return json.dumps(final)
        # return url


if __name__=="__main__":  
    obj =CurrencyExchanger()
    a = obj.currency_exchanger("USD","INR",1000)
    print(a)

