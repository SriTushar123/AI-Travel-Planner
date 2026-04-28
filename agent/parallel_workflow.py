from agent.Nodes import *
from langgraph.graph import StateGraph,START,END
from langchain.messages import HumanMessage

class GraphBuilder():
    def __init__(self):
        self.nodes = Nodes()
    
    def build_graph(self):
        """Builds the final Langgraph workflow"""

        graph = StateGraph(PlannerState)

        graph.add_node("check_country_or_city",self.nodes.check_country_or_city)
        graph.add_node("get_weather",self.nodes.get_weather)
        graph.add_node("get_activities",self.nodes.get_activities)
        graph.add_node("get_restaurents",self.nodes.get_restaurents)
        graph.add_node("get_transportation",self.nodes.get_transportation)
        graph.add_node("get_attractions",self.nodes.get_attractions)
        graph.add_node("get_currency_converter",self.nodes.get_currency_converter)
        graph.add_node("JoinNode",self.nodes.JoinNode)
        graph.add_node("create_itinerary",self.nodes.create_itinerary)

        ## adding the edges
        graph.add_edge(START,"check_country_or_city")

        ## executing all the nodes in parallel
        graph.add_edge("check_country_or_city","get_weather")
        graph.add_edge("check_country_or_city","get_activities")
        graph.add_edge("check_country_or_city","get_restaurents")
        graph.add_edge("check_country_or_city","get_transportation")
        graph.add_edge("check_country_or_city","get_attractions")
        graph.add_edge("check_country_or_city","get_currency_converter")

        ## connecing all the nodes to final itinerary creation node
        graph.add_edge("get_weather","create_itinerary")
        graph.add_edge("get_activities","create_itinerary")
        graph.add_edge("get_restaurents","create_itinerary")
        graph.add_edge("get_transportation","create_itinerary")
        graph.add_edge("get_attractions","create_itinerary")
        graph.add_edge("get_currency_converter","create_itinerary")

        ## Ending the workflow
        # graph.add_edge("JoinNode","create_itinerary")
        graph.add_edge("create_itinerary",END)
        # graph.add_edge("JoinNode",END)

        ## Compiling the graph
        self.workflow = graph.compile()

        return self.workflow
    
    def __call__(self):
        return self.build_graph()

if __name__=="__main__":
    obj = GraphBuilder()
    workflow= obj()
    location = input("Enter Location: ")
    budget = float(input("Enter budget: "))
    days = int(input("Enter days: "))
    start_date = input("Enter start date: ")
    initial_state = {"location":location,"budget":budget,"start_date":start_date,"days":days}
    final_state = workflow.invoke(initial_state)
    print(final_state["final_itinerary"])
    print(type(final_state["final_itinerary"]))