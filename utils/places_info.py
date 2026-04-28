from langchain_google_community import GooglePlacesAPIWrapper,GooglePlacesTool
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json

class GooglePlacesInfo():
    def __init__(self):
        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=os.getenv("GOOGLE_PLACES_API_KEY"))
        self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
    
    def search_activites(self,place)->list:
        """Searches for top 5 activites to do in place"""

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        params = {
            "query":f"activities in  {place}",
            "key":api_key
        }

        response = requests.get(url,params=params)
        data = response.json()

        final_places =[]
        for places in data["results"][:5]:
            final_places.append({
                "name":places["name"],
                "rating":places["rating"]
            })

        return json.dumps({
            "status":"success",
            "data":{
                "query":f"What are the top activities to do in {place}",
                "activities":final_places
            }
        })
    
    def search_restaurents(self,place)->list:
        """Searches for top 5 restaurents in place"""

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        params = {
            "query":f"restaurents in {place}",
            "key":api_key
        }

        response = requests.get(url,params=params)
        data = response.json()

        final_places =[]
        for places in data["results"][:5]:
            final_places.append({
                "name":places["name"],
                "rating":places["rating"]
            })

        return json.dumps({
            "status":"success",
            "data":{
                "query":f"What are the top restaurents in {place}",
                "restaurents":final_places
            }
        })

    def search_transportation(self,place)->list:
        """Returns modes of transportation"""

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        params = {
            "query":f"Transportation in {place}",
            "key":api_key
        }

        response = requests.get(url,params=params)
        data = response.json()

        final_places =[]
        for places in data["results"][:5]:
            final_places.append({
                "name":places["name"],
                "rating":places["rating"]
            })

        return json.dumps({
            "status":"success",
            "data":{
                "query":f"What are the different modes of transportation in {place}",
                "modes of transportation":final_places
            }
        })

    
    def search_attractions(self,place)->list:
        """Returns top 5 attractions in place"""

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        params = {
            "query":f"Attractions in {place}",
            "key":api_key
        }

        response = requests.get(url,params=params)
        data = response.json()

        final_places =[]
        for places in data["results"][:5]:
            final_places.append({
                "name":places["name"],
                "rating":places["rating"]
            })

        return json.dumps({
            "status":"success",
            "data":{
                "query":f"What are the top attractions in {place}",
                "attractions":final_places
            }
        })
    
if __name__=="__main__":
    
    obj = GooglePlacesInfo()
    print(obj.search_activites("Sydney"))
    # print(obj.search_restaurents("Delhi"))