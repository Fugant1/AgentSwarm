from agent_swarm.utils.rag_pipelines import RagPipeline
import logging

class KnowledgeAgent:
    def __init__(self, key):
        self.llm = 'gemini-2.0-flash-thinking-exp-01-21'
        self.temperature = 0
        self.urls = [
              "https://www.infinitepay.io",
              "https://www.infinitepay.io/maquininha",
              "https://www.infinitepay.io/maquininha-celular",
              "https://www.infinitepay.io/tap-to-pay",
              "https://www.infinitepay.io/pdv",
              "https://www.infinitepay.io/receba-na-hora",
              "https://www.infinitepay.io/gestao-de-cobranca-2",
              "https://www.infinitepay.io/link-de-pagamento",
              "https://www.infinitepay.io/loja-online",
              "https://www.infinitepay.io/boleto",
              "https://www.infinitepay.io/conta-digital",
              "https://www.infinitepay.io/pix",
              "https://www.infinitepay.io/emprestimo",
              "https://www.infinitepay.io/cartao",
              "https://www.infinitepay.io/rendimento",
        ]
        self.RAG = RagPipeline(self.llm, key, self.temperature, self.urls)

    async def setup(self):
        await self.RAG.setup()

    async def chat(self, query: str):
        logging.INFO("p")
        await self.setup()
        logging.INFO("p")
        result = await self.RAG.query(query)
        return {
            "response": result["response"],
            "source_context": result["source_documents"]
        }