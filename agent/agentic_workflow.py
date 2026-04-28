from utils.model_loader import ModelLoader
from tools.currency_converter_tool import ConvertCurrency
from tools.weather_info_tool import WeatherInformation
from tools.expense_calculator_tool import ExpenseCalculator
from tools.places_info_tool import PlacesInfo
from langgraph.graph import StateGraph,MessagesState,START,END
from prompts.promp_library import SYSTEM_PROMPT
from langgraph.prebuilt import tools_condition,ToolNode
from langchain.messages import HumanMessage,AIMessage,SystemMessage
from pydantic import BaseModel
from typing import List,Optional
import json


class Place(BaseModel):
    name: str
    description: str

class DayPlan(BaseModel):
    day:int
    title : str
    activities: List[str]
    places: List[Place]

class Budget(BaseModel):
    accommodation: float
    food: float
    transport: float
    activities: float
    miscellaneous: float
    total: float

class TravelItinerary(BaseModel):
    destination_overview: str
    destination_name: str
    itinerary: List[DayPlan]
    transportation: List[str]
    budget_breakdown: Budget

class GraphBuilder():
    def __init__(self,model_provider:str="openai"):
        self.model_provider = ModelLoader(model_provider=model_provider)
        self.llm = self.model_provider.load_model()

        self.tools =[]

        self.currecy_converter = ConvertCurrency()
        self.weather_info = WeatherInformation()
        self.expense_calc = ExpenseCalculator()
        self.places_tools = PlacesInfo()

        self.tools.extend([
            *self.currecy_converter.currency_converter_tool,
            *self.weather_info.weather_info_tool,
            *self.expense_calc.calculator_tools_list,
            *self.places_tools.places_tool
        ])

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.formatter_llm = self.llm.with_structured_output(TravelItinerary)
        self.system_prompt = SYSTEM_PROMPT
        
    
    def agent_function(self,state:MessagesState):
        user_query = state["messages"]
        user_input = [self.system_prompt] + user_query

        ai_response = self.llm_with_tools.invoke(user_input)

        return {"messages":[ai_response]}
    
    def output_formatter(self,state:MessagesState):
        structured_response = self.formatter_llm.invoke(state["messages"])
        structured_response_json_string = structured_response.model_dump_json()

        return {"messages":[AIMessage(content=structured_response_json_string)]}

    def route_after_agent(self,state:MessagesState):
        last_message = state["messages"][-1]

        if hasattr(last_message,"tool_calls") and last_message.tool_calls:
            return "tools"
        else:
            return "output_formatter"

    def joinNode(self):
        pass 
    
    def build_graph(self):
        graph = StateGraph(MessagesState)
        
        ## Adding Nodes
        graph.add_node("agent",self.agent_function)
        graph.add_node("tools",ToolNode(tools=self.tools))
        graph.add_node("output_formatter",self.output_formatter)

        ## Adding Edges
        graph.add_edge(START,"agent")
        graph.add_conditional_edges("agent",self.route_after_agent,{"tools":"tools","output_formatter":"output_formatter"})
        graph.add_edge("tools","agent")
        graph.add_edge("output_formatter",END)

        self.workflow = graph.compile()

        return self.workflow
    
    def __call__(self):
        return self.build_graph()



if(__name__=="__main__"):
    obj = GraphBuilder()
    workflow = obj()
    destination = input("Enter Travel Destination: ")
    start_date = input("Enter the start date: ")
    days = int(input("Enter number of days: "))
    budget = float(input("Enter the budget for the trip: "))

    initial_state = {"messages":[HumanMessage(content=f"Give me travel itinerary for {destination},the budget is {budget} INR\nStart Date: {start_date}\nNumber of days:{days}")]}
    final_state = workflow.invoke(initial_state)
    output = json.loads(final_state["messages"][-1].content)
    # print(final_state)
    print(type(output))
    print(output)

