import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json
from datetime import date,datetime,timedelta
from dateutil import parser
from pydantic import BaseModel,Field
from typing import Annotated,Literal
from langchain_openai import ChatOpenAI


class Climate(BaseModel):
    climate : Annotated[Literal["Cold","Cool","Mild","Warm","Hot"],Field(description="The climate of the place")]

class DateOutput(BaseModel):
    max_temp: Annotated[float,Field(description="Returns the maximum tempaerature of the place on that day")]
    min_temp: Annotated[float,Field(description="Returns the maximum tempaerature of the place on that day")]


class WeatherInfo():
    def __init__(self):
        self.base_url = "http://api.weatherapi.com/v1"
        self.api_key = os.getenv("WEATHER_API_KEY")


    def get_forecast_within_3_days(self,place:str,date:str):
        """Returns the max and min temp of the given date which is within 3 days from today's date """

        date = parser.parse(date)
        url = f"{self.base_url}/forecast.json"
        params = {
            "key":self.api_key,
            "q":place,
            "dt":date
        }

        response = requests.get(url=url,params=params)
        if response.status_code != 200:
            raise Exception(
        f"API Call Failed | Status: {response.status_code} | Response: {response.text} | place:{place}")
        data = response.json()

        return {
            "date":data["forecast"]["forecastday"][0]["date"],
            "max_temp_centrigrade":data["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
            "min_temp_centrigrade":data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
        }
    
    def get_forecast_beyond_3_days(self,place:str,date:str):
        """Returns the max and min temp of the given date which is beyond 3 days from today's date using a LLM"""

        date = parser.parse(date)
        model = ChatOpenAI(model="gpt-4.1-mini")
        model = model.with_structured_output(DateOutput)

        response = model.invoke(f"What is the maximum and minimum temperature of the {place} on {date} in centigrade.")

        date = date.strftime("%Y-%m-%d")

        return {
            "date":date,
            "max_temp_centrigrade":response.max_temp,
            "min_temp_centrigrade":response.min_temp,
        }


    def get_weather_forecast(self,place:str,start_date:str,days:int):
        """Returns the max and min temp from the start date for the number of days"""

        start_date = parser.parse(start_date)
        end_date = start_date + timedelta(days=days-1)

        date_today = parser.parse(datetime.now().strftime("%Y-%m-%d"))
        date_3_day = date_today + timedelta(days=3)

        temp =[]
        while(start_date<=end_date):

            if (start_date>=date_today and start_date<=date_3_day):
                temp.append(self.get_forecast_within_3_days(place=place,date=start_date.strftime("%Y-%m-%d")))
            else:
                temp.append(self.get_forecast_beyond_3_days(place=place,date=start_date.strftime("%Y-%m-%d")))

            start_date = start_date + timedelta(days=1)
        
        return json.dumps({
            "status":"success",
            "data":{
                "place":place,
                "temperature with date":temp
            }
        })

    def get_climate(self,place:str,date:str):
        """Return the climate of the place in the month of the date"""

        date = parser.parse(date)
        month = date.strftime("%B")
        model = ChatOpenAI(model="gpt-4.1-mini")
        model = model.with_structured_output(Climate)

        response = model.invoke(f"What is usually the climate of {place} in the month of {month}")

        return json.dumps({
            "status":"success",
            "data":{
                "place":place,
                "climate":response.climate
            }
        })


if __name__=="__main__":  
    obj = WeatherInfo()
    # print(obj.get_weather_forecast(place="Delhi",start_date="2026-09-2",days=4))
    # res = obj.get_forecast_beyond_3_days(place="Delhi",date="2026-05-01")
    # print(res)
    print(obj.get_weather_forecast("Tokyo","2026-06-29",5))