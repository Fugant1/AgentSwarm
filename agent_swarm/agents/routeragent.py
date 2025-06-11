from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

key = os.getenv('OPEN_API_KEY')

class RouterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(key, temperature=0) #temp zero to more accurate responses
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Classify the message as either 'knowledge', 'support', or 'pokemon'. Just return the word with no explain"),
            ("human", "Message: {message}") #tried a prompt that make the model answer one word
        ]) #added pokemon category for testing/extensibility ¯\_(ツ)_/¯

    async def route(self, message: str):
        chain = self.prompt | self.llm
        result = await chain.ainvoke({"message": message})
        answer = result.content.lower() #lower to be easier to identify

        if 'knowledge' in answer: #verifying the hole message for safety
            return 'knowledge'
        elif 'support' in answer:
            return 'support'
        elif 'pokemon' in answer:
            return 'pokemon'
        
#this class is just a router, simple as it needs to be