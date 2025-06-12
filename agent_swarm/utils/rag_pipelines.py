from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser
import logging

class RagPipeline:
    def __init__(self, model_name, key, temperature, urls):
        self.key = key
        self.urls = urls
        self.model_name = model_name
        self.temperature = temperature
        self.vectorstore = None
        self.retriever = None
        self.rag_chain = None
        self.llm = None
    
    async def setup(self):
        documents = await self._load_documents()
        self.vectorstore = self._create_vectorstore(documents)
        self.retriever = self.vectorstore.as_retriever()
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=self.key
        )
        self.prompt = ChatPromptTemplate.from_template(
            "You are a helpful assistant. Use the following context to answer the question.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}"
        )
        self.rag_chain = (
            RunnableMap({
                "question": lambda x: x["question"]
            })
            | RunnableLambda(self._add_context)
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    async def _load_documents(self):
        loader = WebBaseLoader(self.urls)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        return splitter.split_documents(docs)

    def _create_vectorstore(self, chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=self.key)
        return FAISS.from_documents(chunks, embeddings)
    
    async def _add_context(self, inputs: dict):
        question = inputs["question"]
        logging.INFO(question)
        docs = await self.retriever.aget_relevant_documents(question)
        context = "\n\n".join(doc.page_content.replace("{", "{{").replace("}", "}}") for doc in docs)
        return {
            "question": question,
            "context": context
        }

    async def query(self, user_input: str):
        if not self.rag_chain:
            raise ValueError("RAG pipeline not initialized. Call `setup()` first.")
        logging.INFO(user_input)
        result = await self.rag_chain.ainvoke({"question": user_input})
        return {
            "response": result,
            "source_documents": []
        }