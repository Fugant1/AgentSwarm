from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RouterAgent:
    def __init__(self, key):
        os.environ['USER_AGENT'] = 'AgentSwarmRouter/1.0'
        self.llm = ChatGoogleGenerativeAI(google_api_key=key,
            model="gemini-2.0-flash-thinking-exp-01-21", 
            temperature=0,
            max_output_tokens=1000, 
            top_k=1,
            top_p=0) 
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Classify the message as either 'knowledge', 'support', or 'pokemon'. Just return the word with no explain"),
            ("human", "Message: {message}") #tried a prompt that make the model answer one word
        ]) #added pokemon category for testing/extensibility ¯\_(ツ)_/¯

    async def route(self, message: str):
        chain = self.prompt | self.llm
        result = await chain.ainvoke({"message": message})
        answer = result.content.lower() #lower to be easier to identify
        logger.info(f"Classification result: {answer}") 

        if 'knowledge' in answer: #verifying the hole message for safety
            return 'knowledge'
        elif 'support' in answer:
            return 'support'
        elif 'pokemon' in answer:
            return 'pokemon'
        
#this class is just a router, simple as it needs to be