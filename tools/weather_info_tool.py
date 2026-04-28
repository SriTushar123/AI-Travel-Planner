from langchain.tools import tool
from utils.weather_info import WeatherInfo


class WeatherInformation():

    def __init__(self):
        self.weather_info = WeatherInfo()
        self.weather_info_tool = self._setup_tools()

    
    def _setup_tools(self):
        """Returns the list of all the tools required for weather conversion"""

        @tool
        def get_weather_info(place,start_date,days)->str:
            """Returns the max and min temperature of the place given by the user from start date for number of days"""

            return self.weather_info.get_weather_forecast(place=place,start_date=start_date,days=days)

            
        return [get_weather_info]
    


if __name__=="__main__":
    obj = WeatherInformation()
    print(obj._setup_tools())
     