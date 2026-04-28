from langchain.tools import tool
from utils.places_info import GooglePlacesInfo

class PlacesInfo():

    def __init__(self):
        self.places_info = GooglePlacesInfo()
        self.places_tool = self._setup_tools()
    
    def _setup_tools(self):
        """Returns the list of tools for information on places"""

        @tool
        def get_activities(place):
            
            """Return the top activities to do in the place given by the user"""

            return self.places_info.search_activites(place=place)
        
        @tool
        def get_restaurents(place):

            """Return the top restaurents in the place given by the user"""

            return self.places_info.search_restaurents(place=place)

        @tool
        def get_transportation(place):

            """Return the top modes of transport in the place given by the user"""

            return self.places_info.search_restaurents(place=place)
        
        @tool
        def get_attractions(place):

            """Return the top 5 attractions in the place given by the user"""

            return self.places_info.search_attractions(place=place)


        return [get_activities,get_restaurents,get_transportation,get_attractions]


if(__name__=="__main__"):
    obj = PlacesInfo()
    print(obj._setup_tools())
