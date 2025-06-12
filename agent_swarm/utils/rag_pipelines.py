from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
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
        logging.info("cheguei aqui")
        documents = await self._load_documents()
        logging.info("ENA1")
        self.vectorstore = self._create_vectorstore(documents)
        logging.info("ENA2")
        self.retriever = self.vectorstore.as_retriever()
        logging.info("ENA3")
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=self.key
        )
        prompt_template = PromptTemplate.from_template(
            """You are a helpful assistant. Use the following context to answer the question.

            Context:
            {context}

            Question: {question}
            """
        )
        self.rag_chain = RunnableSequence(
            self._format_inputs,
            self.retriever | self._format_context,
            prompt_template,
            self.llm
        )
        logging.info("ENF")

    async def _load_documents(self):
        loader = WebBaseLoader(self.urls)
        docs = await loader.aload()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        return splitter.split_documents(docs)

    def _create_vectorstore(self, chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=self.key)
        return FAISS.from_documents(chunks, embeddings)

    def _format_inputs(self, inputs):
        return inputs["question"]

    def _format_context(self, docs):
        context = "\n\n".join(doc.page_content for doc in docs)
        return {"context": context}

    async def query(self, user_input: str):
        if not self.rag_chain:
            raise ValueError("RAG pipeline not initialized. Call `setup()` first.")
        result = await self.rag_chain.ainvoke({"question": user_input})
        return {"response": result}