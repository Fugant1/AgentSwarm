from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class Personalities:
    def __init__(self):
        self.personality_llm = ChatOpenAI(temperature = 0.7, model = 'gpt-3.5')

    async def apply_knwoledge_personality(self, question, raw_response):
        prompt = ChatPromptTemplate('''
        You are a friendily experte assisstant for a fintech company called infinitePay,
        The user questioned about: {question};
        Your teammate gave this factual response: "{raw_response}";
        Rewrite this response in a helpful, informal, slightly enthusiastic tone, and mention InfinitePay if relevant.
        Keep it short and clear.
        ''')
        chain = prompt | self.personality_llm
        response = await chain.ainvoke({'question': question, 'raw_response': raw_response})
        return response.content

    async def apply_costumer_personality(self, question, raw_response):
        prompt = ChatPromptTemplate('''

        ''')
        chain = prompt | self.personality_llm
        response = await chain.ainvoke({'question': question, 'raw_response': raw_response})
        return response.content

    async def apply_pokemon_personality(self, question, raw_response):
        prompt = ChatPromptTemplate('''

        ''')
        chain = prompt | self.personality_llm
        response = await chain.ainvoke({'question': question, 'raw_response': raw_response})
        return response.content