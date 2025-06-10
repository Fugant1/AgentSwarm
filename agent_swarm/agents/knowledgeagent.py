from agent_swarm.utils.rag_pipelines import RagPipeline

class KnowledgeAgent:
    def __init__(self):
        self.llm = 'gpt-3.5'
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
        self.RAG = RagPipeline(self.llm, self.temperature, self.urls)

    async def setup(self):
        await self.RAG.setup()

    async def chat(self, query: str):
        result = await self.RAG.query(query)
        return {
            "response": result["response"],
            "source_context": result["source_documents"]
        }