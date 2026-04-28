from langchain.tools import tool
from utils.currency_converter import CurrencyExchanger

class ConvertCurrency():
    def __init__(self):
        self.currency_exchanger = CurrencyExchanger()
        self.currency_converter_tool = self._setup_tools()

    def _setup_tools(self):
        """Set up all the tools from the Currency Exchanger"""

        @tool
        def give_amount_in_new_currency(from_currency:str,to_currency:str,amount:float):
            """Takes a currency from the user, converts it into another currency (forex rate) and then multiplies the amount by the forex rate"""

            return self.currency_exchanger.currency_exchanger(from_currency=from_currency,to_currency=to_currency,amount=amount)
        
        return [give_amount_in_new_currency]

    # def give_amount_in_new_currency(self,from_currency:str,to_currency:str,amount:float):
    #         """Takes a currency from the user, converts it into another currency (forex rate) and then multiplies the amount by the forex rate"""

    #         return self.currency_exchanger.currency_exchanger(from_currency=from_currency,to_currency=to_currency,amount=amount)
        
if (__name__=="__main__"):
    obj = ConvertCurrency()
    print(obj._setup_tools())