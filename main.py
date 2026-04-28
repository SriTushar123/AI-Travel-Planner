from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
from agent.parallel_workflow import GraphBuilder
from langchain.messages import HumanMessage
from typing import Annotated
import json

app = FastAPI()

# ✅ CORS (already correct)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    location: str
    start_date: str
    budget: Annotated[float,Field(description="Budget of the entire trip",gt=0)]
    days: Annotated[int,Field(description="No of days of the trip",gt=0)]


@app.post("/plan-trip")
def enter_details(details: TripRequest):
    try:
        obj = GraphBuilder()
        workflow = obj()

        initial_state = {"location":details.location,"budget":details.budget,"start_date":details.start_date,"days":details.days}

        final_state = workflow.invoke(initial_state)
        output = final_state["final_itinerary"]

        return output

    except Exception as e:
        return {"error": str(e)}