import math
import os
import sys
import logging
from termcolor import colored

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, ConversationChain
from langchain.retrievers import BM25Retriever, EnsembleRetriever, MultiQueryRetriever, ContextualCompressionRetriever
from langchain.text_splitter import SpacyTextSplitter
from langchain.vectorstores import FAISS
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.docstore.document import Document
import warnings
import spacy

nlp = spacy.load("en_core_web_sm")

log = logging.getLogger("ChatBot")
logging.basicConfig(level=logging.WARNING)

warnings.filterwarnings('ignore')

os.environ["OPENAI_API_KEY"] = "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"
os.environ["TOKENIZERS_PARALLELISM"] = "TRUE"
# api_key = os.environ.get('OPENAI_API_KEY')

file_path = sys.argv[1]


def log_messages(string):
    print(f" 🤖💬️ {string}")


class FormatPrint:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    START = '\033[1m'


class PDFChatbot:
    def __init__(self, file_path):
        log_messages(f'FileLoad|{file_path}|Attempting')
        try:
            self.document = PyPDFLoader(file_path=file_path).load()
            log_messages(f'FileLoad|{file_path}|Successful')
        except:
            if not os.path.exists(file_path):
                log_messages("File not found, please try with another file")
            else:
                log_messages('Unable to open file, please check the integrity of the file')

        log_messages("TextSplitter|Instantiation|Start")
        full_text = ''
        for sub_doc in self.document:
            full_text += ' ' + sub_doc.page_content

        length_chunk = int(nlp.max_length * 0.8)
        length_total = len(full_text)

        full_texts = [full_text[i:i + length_chunk] for i in range(0, length_total, length_chunk)]

        # Keeping the prompt simpel and to the point to ensure lower occurrence of hallucinations
        self.prompt_template = """Answer the following question based on the context only and nothing else. 
                            if the user is asking for instructions, return the answer as bullets
                            context: {context}
                            question: {user_input}
                            answer: """
        self.prompt_template = PromptTemplate.from_template(template=self.prompt_template)

        self.documents = [Document(page_content=x, metadata={"source": file_path}) for x in full_texts]
        self.text_splitter = SpacyTextSplitter(pipeline='en_core_web_sm', chunk_overlap=256)
        log_messages("TextSplitter|Instantiation|End")

        # Splitting the documenting and augmenting the metadata for reference purposes
        log_messages("TextSplitter|split_documents|Start")
        self.documents = self.text_splitter.split_documents(documents=self.documents)
        self.documents = [self.document_metadata(document=document) for document in self.documents]
        log_messages("TextSplitter|split_documents|End")

        # initiate the chat model
        self.chat_model = None
        self.chat_load()

        # declare the retriever variable and load them
        self.bm25_retriever = None
        self.embedding = None
        self.faiss_retriever = None
        self.vectorstore = None
        self.multiquery_retriever = None
        self.compressor = None
        self.compression_retriever = None
        self.multiquery_retriever = None
        self.ensemble_retriever = None
        self.retrievers_load()

        # define the llm chain
        self.llm_chain = LLMChain(llm=self.chat_model, prompt=self.prompt_template)

    @staticmethod
    def document_metadata(document: Document) -> Document:
        page_content = document.page_content
        metadata_new = {'source': document.metadata['source'], "page_content_original": page_content}
        return Document(page_content=page_content, metadata={"metadata": metadata_new})

    def chat_load(self):
        log_messages("ChatOpenAI|Model|loading|")
        self.chat_model = ChatOpenAI()
        log_messages("ChatOpenAI|model|loaded|")

    def retrievers_load(self):
        # self.bm25_retriever = BM25Retriever.from_documents(self.documents)
        # self.bm25_retriever.k = 5
        self.embedding = OpenAIEmbeddings()
        self.vectorstore = FAISS.from_documents(documents=self.documents, embedding=self.embedding)
        self.faiss_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        self.multiquery_retriever = MultiQueryRetriever.from_llm(retriever=self.vectorstore.as_retriever(),
                                                                 llm=self.chat_model)
        self.compressor = LLMChainExtractor.from_llm(self.chat_model)
        self.compression_retriever = ContextualCompressionRetriever(base_compressor=self.compressor,
                                                                    base_retriever=self.multiquery_retriever)

        # Assemble the retriever. The weights here are chosen so that the compression retriever gets more weight
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.compression_retriever, self.faiss_retriever],
            weights=[0.7, 0.3])

    def get_top_documents(self, query):
        return self.ensemble_retriever.get_relevant_documents(query=query)


pdf_chatbot = PDFChatbot(file_path=file_path)

while True:
    user_input = input(" 🤖💬️ Enter Your Query: ")
    if user_input == "exit":
        log_messages("Thank you for using our Chat service. Have a great day!!")
        exit()
    else:
        contexts = pdf_chatbot.get_top_documents(user_input)
        if len(contexts) > 0:
            context_compressed = ' '.join(contexts[0].page_content.split())
            context_original = ' '.join(contexts[0].metadata['metadata']['page_content_original'].split())
            context_original = f"ⓘ From {contexts[0].metadata['metadata']['source']} || {context_original}"
            output = pdf_chatbot.llm_chain(inputs={'context': context_compressed, 'user_input': user_input})
            print(f"\n{output['text']}", end='\n\n')

            print(
                FormatPrint.START + FormatPrint.BLUE + FormatPrint.BOLD + "Compressed Context: " + FormatPrint.BOLD
                + FormatPrint.BLUE + FormatPrint.END,
                end='')
            print(f"{context_compressed}", end='\n\n')

            print(
                FormatPrint.START + FormatPrint.GREEN + FormatPrint.BOLD + "Original Context: " + FormatPrint.BOLD
                + FormatPrint.GREEN + FormatPrint.END,
                end='')
            print(f"{context_original} ", end='\n\n')
        else:
            print("Cannot answer the question given that there were not relevant documents returned, please try again")
