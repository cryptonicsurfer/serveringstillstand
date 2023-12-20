from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import streamlit as st 
from pathlib import Path
from llama_index import download_loader
from llama_index import Document
import pandas as pd


def load_content_from_csv(file_path, colnum):
    df = pd.read_csv(file_path)
    content_array = df.iloc[:, colnum].to_list()  # Assumes the content is in the second column
    return content_array

csv_file_path = 'concatenated_content.csv'  # Replace with your CSV file path
text_list = load_content_from_csv(csv_file_path, 1)
url_list = load_content_from_csv(csv_file_path, 0)

# Set up the Qdrant client
url = 'qdrant.utvecklingfalkenberg.se'
api_key = st.secrets["QDRANT_API_KEY"]
client = QdrantClient(url=url, api_key=api_key, port=443)
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

# Load documents

documents = []
for text, url in zip(text_list, url_list):
    doc = Document(text=text, metadata={"url": url})
    documents.append(doc)

# Create QdrantVectorStore
vector_store = QdrantVectorStore(client=client, collection_name="alkohollagen_update2")

# Create the storage and service contexts
llm = OpenAI(temperature=0.0, model='gpt-4-1106-preview')
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(llm=llm)

# Build the VectorStoreIndex
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)

# Create a query engine and query
# query_engine = index.as_query_engine(streaming = True, similarity_top_k=5)
# response = query_engine.query("Vad är viktigt att tänka på när det gäller serveringstillstånd? Inkludera alltid källhänvisning för var du hittar information till dina svar")
# response.print_response_stream()


