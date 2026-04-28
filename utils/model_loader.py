from pydantic import BaseModel,Field
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from utils.config_loader import config_loader
from typing import Literal,Annotated,Optional
from dotenv import load_dotenv
load_dotenv()
import os


class ConfigLoader():
    def __init__(self):
        self.config = config_loader()
    
    def __getitem__(self, key):
        return self.config[key]
    


class ModelLoader():
    def __init__(self,model_provider:str="openai"):
        self.model_provider = model_provider
        self.config = ConfigLoader()
    
    def load_model(self):    

        if self.model_provider == "Google":
            api_key = os.getenv("GOOGLE_API_KEY")
            model_name = self.config["llm"]["google"]["model_name"]
            model = ChatGoogleGenerativeAI(model=model_name,api_key=api_key)
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            model = ChatOpenAI(model=model_name,api_key=api_key)
        
        return model


if __name__=="__main__":
    obj = ModelLoader()
    model = obj.load_model()

    response = model.invoke("What is the capital of India")
    print(response.content)