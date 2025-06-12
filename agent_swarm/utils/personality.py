from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

class Personalities:
    def __init__(self, key):
        self.llm = ChatGoogleGenerativeAI(google_api_key=key,
            model="gemini-2.0-flash-thinking-exp-01-21", 
            temperature=0.7) 

    async def apply_knwoledge_personality(self, question, raw_response):
        prompt = ChatPromptTemplate.from_messages('''
        You are a friendily experte assisstant for a fintech company called infinitePay,
        The user questioned about: {question};
        Your teammate gave this factual response: "{raw_response}";
        Rewrite this response in a helpful, informal, slightly enthusiastic tone, and mention InfinitePay if relevant.
        Keep it short and clear.
        ''')
        messages = self.prompt.format_messages(question=question, raw_response = raw_response)
        result = await self.llm.ainvoke(messages)
        return result.content

    async def apply_costumer_personality(self, question, raw_response):
        prompt = ChatPromptTemplate.from_messages('''

        ''')
        messages = self.prompt.format_messages(question=question, raw_response = raw_response)
        result = await self.llm.ainvoke(messages)
        return result.content

    async def apply_pokemon_personality(self, question, raw_response):
        prompt = ChatPromptTemplate.from_messages('''

        ''')
        messages = self.prompt.format_messages(question=question, raw_response = raw_response)
        result = await self.llm.ainvoke(messages)
        return result.content