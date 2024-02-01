import os
from dotenv import load_dotenv
import openai
from qdrant_client import QdrantClient
from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex, ServiceContext, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
import chainlit as cl

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up the Qdrant client
url = 'qdrant.utvecklingfalkenberg.se'
api_key = os.getenv("QDRANT_API_KEY")  # Ensure this is set in your .env file
client = QdrantClient(url=url, api_key=api_key, port=443)

# Configure the OpenAI model for use with llama_index
llm = OpenAI(temperature=0.1, model="gpt-4-1106-preview")

# Create QdrantVectorStore
vector_store = QdrantVectorStore(client=client, collection_name="businesshalland")

# Create the storage and service contexts
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(llm=llm)

# Build the VectorStoreIndex
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, service_context=service_context)

@cl.on_chat_start
async def factory():
    # Assume the setup for llm_predictor and service_context is done here
    # And query_engine is instantiated and set in the session as shown previously
    query_engine = index.as_query_engine(service_context=service_context, streaming=True, similarity_top_k=4)
    cl.user_session.set("query_engine", query_engine)

@cl.on_message
async def main(message: cl.Message):
    # Retrieve the query_engine from the session
    query_engine = cl.user_session.get("query_engine")
    if query_engine is None:
        # Handle the case where query_engine is not found in the session
        await message.reply("An error occurred: query engine not initialized.")
        return

    user_input = message.content
    # Format the query with specific instructions and the user input
    formatted_query = f"System instructions: Svara koncist men detaljerat. Inkludera alltid var du hittat information tex URL. Frågan som du svarar på: {user_input}."

    # Query the engine with the formatted input
    response = await cl.make_async(query_engine.query)(formatted_query)

    response_message = cl.Message(content="")
    print(response_message)

    # Process and send the response
    for token in response.response_gen:
        await response_message.stream_token(token=token)

    if response.response_txt:
        response_message.content = response.response_txt

    await response_message.send()
