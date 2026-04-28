from utils.model_loader import ModelLoader
from typing import Annotated,Dict,TypedDict
import operator
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from utils.utilities import *
from datetime import datetime,date,timedelta
from dateutil import parser
import math
from utils.weather_info import WeatherInfo
import json
from utils.places_info import GooglePlacesInfo
from utils.currency_code import get_currency_code
from utils.currency_converter import CurrencyExchanger
from prompts.promp_library import itinerary_generator_prompt
import operator

class PlannerState(TypedDict):
    location: str
    budget: float 
    start_date: str
    days: int
    cities: list[str]
    result : Annotated[dict,operator.or_]
    # weather_info : list[dict]
    # activities :list[dict]
    # restaurents: list[dict]
    # transportation: list[dict]
    # attractions: list[dict]
    # exchange_rate: float
    final_itinerary: dict
    

class Nodes():
    def __init__(self):
        self.model_obj = ModelLoader()
        self.model = self.model_obj.load_model()
    
    def check_country_or_city(self,state:PlannerState)->PlannerState:
        """Checks wether the entered location by the user is a country or just a city"""
        location = state["location"]

        location = location[0].upper() + location[1:]
        
        if location in countries:
            model = self.model.with_structured_output(Cities)
  
            city = model.invoke(f"What are the two top cities in {state['location']}")

            return {"cities":[city.city1,city.city2]}
        
        else:
            return {"cities":[location]}

    def get_weather(self,state:PlannerState):
        """Returns the weather"""

        temperatures = []
        weather = WeatherInfo()
        if (len(state["cities"])>1):
            start_date = parser.parse(state["start_date"])
            first_city_days = int(math.ceil(state["days"]/2))
            # print(f"first_city_days: {first_city_days}")
            second_city_start_date = start_date + timedelta(days=first_city_days)
            # print(f"second_city_start_date: {second_city_start_date}")
            second_city_days = state["days"] - first_city_days
            # print(f"second_city_days :{second_city_days}")
            travel_dates = [start_date.strftime("%Y-%m-%d"),second_city_start_date.strftime("%Y-%m-%d")]
            travel_days = [first_city_days,second_city_days]
            
            for i in range (0,2):
                output = weather.get_weather_forecast(place=state["cities"][i],start_date=travel_dates[i],days=travel_days[i])
                output = json.loads(output)
                res =[]
                for temp in output["data"]["temperature with date"]:
                    res.append({
                        "date":temp["date"],
                        "max_temp_centrigrade":temp["max_temp_centrigrade"],
                        "min_temp_centrigrade": temp["min_temp_centrigrade"]
                    })
                temperatures.append({
                    f"{state["cities"][i]}":res
                })
        else:

            output = weather.get_weather_forecast(place=state["location"],start_date=state["start_date"],days=state["days"])
            output = json.loads(output)
            res =[]
            for temp in output["data"]["temperature with date"]:
                res.append({
                    "date":temp["date"],
                    "max_temp_centrigrade":temp["max_temp_centrigrade"],
                    "min_temp_centrigrade": temp["min_temp_centrigrade"]
                })
            temperatures.append({
                f"{state["cities"][0]}":res
            })

        return {"result":{"weather_info":temperatures}}
        # return {"result":[{"weather_info":temperatures}]}

    def get_activities(self,state:PlannerState):
        """Returns the top 5 activities to perform in the respective cities"""

        activities =[]
        activities_obj = GooglePlacesInfo()
        for city in state["cities"]:
            output = json.loads(activities_obj.search_activites(place=city))
            activities.append({
                f"{city}" : output["data"]["activities"]
            })
        
        return {"result":{"activities":activities}}
        # return {"result":[{"activities":activities}]}
    
    def get_restaurents(self,state:PlannerState):
        """Returns the top 5 restaurents in the respective cities"""

        restaurents =[]
        restaurents_obj = GooglePlacesInfo()
        for city in state["cities"]:
            output = json.loads(restaurents_obj.search_restaurents(place=city))
            restaurents.append({
                f"{city}" : output["data"]["restaurents"]
            })
        
        return {"result":{"restaurents":restaurents}}
    
    def get_transportation(self,state:PlannerState):
        """Returns the top 5 modes of transportation in the respective cities"""

        transportation =[]
        transportation_obj = GooglePlacesInfo()
        for city in state["cities"]:
            output = json.loads(transportation_obj.search_transportation(place=city))
            transportation.append({
                f"{city}" : output["data"]["modes of transportation"]
            })
        
        return {"result":{"transportation":transportation}}
    
    def get_attractions(self,state:PlannerState):
        """Returns the top 5 attractions in the respective cities"""

        attractions =[]
        attractions_obj = GooglePlacesInfo()
        for city in state["cities"]:
            output = json.loads(attractions_obj.search_attractions(place=city))
            attractions.append({
                f"{city}" : output["data"]["attractions"]
            })
        
        return {"result":{"attractions":attractions}}

    def get_currency_converter(self,state:PlannerState):
        "Gives the forex rate of the country"


        if (len(state["cities"])>1):
            currency_code = get_currency_code(state["location"])
        else:
            model = self.model.with_structured_output(CountryName)
            country_name = model.invoke(f"Return the name of the country this city belongs to {state["cities"][0]}").country_name
            currency_code = get_currency_code(country_name)
        
        if(currency_code=="INR"):
            return {"result":{"rate":0}}
        else:
            currency_obj = CurrencyExchanger()
            output = json.loads(currency_obj.currency_exchanger(from_currency=currency_code,to_currency="INR",amount=0))
            rate = float(output["data"]["conversion_rate"])
        
        return {"result":{"rate":rate}}

    def JoinNode(self,state:PlannerState):
        """Waits for all the nodes to finish execution"""

        return state


    def create_itinerary(self,state:PlannerState):

        prompt = itinerary_generator_prompt.invoke({
            "location" : state["location"],
            "budget" : state["budget"],
            "start_date": state["start_date"],
            "days":state["days"],
            "cities":state["cities"],
            "weather_info":state["result"]["weather_info"],
            "activities":state["result"]["activities"],
            "restaurents":state["result"]["restaurents"],
            "transportation":state["result"]["transportation"],
            "attractions":state["result"]["attractions"],
            "exchange_rate":state["result"]["rate"]
        })

        model = self.model.with_structured_output(Itinerary) 
        response = model.invoke(prompt)
        response = response.model_dump_json()
        
        return {"final_itinerary":json.loads(response)}

    



# if __name__=="__main__":
#     obj = Nodes()
#     st = PlannerState(location="Vietnam",start_date="2026-04-29",days=5,budget=60000)
#     result = obj.check_country_or_city(state=st)
#     # print("The cities are: ", result)
#     # print("")
#     st.update(result)
#     result = obj.get_weather(state=st)
#     st.update(result)
#     st["result"].extend(result)
#     result = obj.get_activities(state=st)
#     st["result"].extend(result)
#     result = obj.get_restaurents(state=st)
#     st["result"].extend(result)
#     result = obj.get_transportation(state=st)
#     st["result"].extend(result)
#     result = obj.get_attractions(state=st)
#     st["result"].extend(result)
#     result = obj.get_currency_converter(state=st)
#     st["result"].extend(result)
#     print(st)
#     print("**************************")
#     print("")
#     print(st["result"])



    # result = obj.get_weather(state=st)
    # print("The weather is: ", result)
    # print("")
    # st.update(result)
    # result = obj.get_activities(state=st)
    # print("The activities are: ", result)
    # st.update(result)
    # print("")
    # result = obj.get_restaurents(state=st)
    # print("The restaurents are: ", result)
    # st.update(result)
    # print("")
    # result = obj.get_transportation(state=st)
    # print("The transportation are: ", result)
    # print("")
    # st.update(result)
    # result = obj.get_attractions(state=st)
    # print("The attractions are: ", result)
    # print("")
    # st.update(result)
    # result = obj.get_currency_converter(state=st)
    # print("The forex is: ", result)
    # print("")
    # st.update(result)
    # print("*************************")
    # print(st)
    # result = obj.create_itinerary(state=st)
    # print("The final itinerary is: ", result)
    # print(type(result))
    # print("")

    
