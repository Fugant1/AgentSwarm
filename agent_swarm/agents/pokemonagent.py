from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
class PokemonAgent:
    def __init__(self, key):
        self.llm = ChatGoogleGenerativeAI(google_api_key=key,
            model="gemini-2.0-flash-thinking-exp-01-21", 
            temperature=0) #zero temp to more precise resposne 
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Pokemon Agent who provide information about pokemon to user"),
            ("human", "Message: {message}")
        ]) 

    async def chat(self, message):
        chain = self.prompt | self.llm
        result = await chain.ainvoke({"message": message})
        
        return result.content