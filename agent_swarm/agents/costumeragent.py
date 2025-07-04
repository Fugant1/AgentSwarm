from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

@tool
def get_customer_balance(customer_id: str):
    '''returns the balance of the user by its ID'''
    fake_db = {"123": "R$ 550,00", "456": "R$ 0,00"} 
    #example of database, it could be in DynamoDB, PostgreSQL or any db, it would just needed to create a class to handle it
    return fake_db.get(customer_id, "Customer not found.")

@tool
def open_support_ticket(issue: str):
    '''Opens a support ticket and returns a reference number'''
    return f"Ticket opened for issue: {issue}. Reference ID: #{hash(issue) % 10000}"

class CostumerAgent:
    def __init__(self, key):
        self.llm = ChatGoogleGenerativeAI(google_api_key=key,
            model="gemini-2.0-flash-thinking-exp-01-21", 
            temperature=0) #zero temp to more precise resposne
 
        self.tools = [get_customer_balance, open_support_ticket]
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

    async def chat(self, message: str):
        return await self.agent.arun(message)