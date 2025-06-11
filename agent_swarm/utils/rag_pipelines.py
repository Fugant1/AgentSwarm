from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
import os

class RagPipeline:
    def __init__(self, temperature, model_name, urls):
        self.key = os.getenv('OPEN_API_KEY')
        self.urls = urls
        self.model_name = model_name
        self.temperature = temperature
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
    
    async def setup(self):
        documents = await self._load_documents()
        self.vectorstore = self._create_vectorstore(documents)
        self.retriever = self.vectorstore.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm = ChatOpenAI(kapi_key=self.key,
                model=self.model_name, 
                temperature=self.temperature, #zero temp to more precise resposne
                max_tokens=1),
            retriever=self.retriever,
            return_source_documents=True
        )

    async def _load_documents(self):
        loader = WebBaseLoader(self.urls)
        docs = await loader.aload()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        return splitter.split_documents(docs)

    def _create_vectorstore(self, chunks):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(chunks, embeddings)

    async def query(self, user_input: str):
        if not self.qa_chain:
            raise ValueError("RAG pipeline not initialized. Call `setup()` first.")
        result = await self.qa_chain.ainvoke(user_input)
        return {
            "response": result["result"],
            "source_documents": result.get("source_documents", [])
        }