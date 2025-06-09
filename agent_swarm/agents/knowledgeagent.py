from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader

class KnowledgeAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.vectorstore = None
        self.qa_chain = None

    async def setup(self):
        self.vectorstore = await self._load_vectorstore()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever()
        )

    async def _load_vectorstore(self):
        urls = [
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
        loader = WebBaseLoader(urls)
        docs = await loader.aload()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(chunks, embeddings)

    async def handle(self, query: str):
        result = await self.qa_chain.ainvoke(query)
        return {
            "response": result["result"],
            "source_context": result.get("source_documents", [])
        }