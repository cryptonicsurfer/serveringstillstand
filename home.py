from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import streamlit as st
# Set up the Qdrant client
url = 'qdrant.utvecklingfalkenberg.se'
api_key = st.secrets["QDRANT_API_KEY"]
client = QdrantClient(url=url, api_key=api_key, port=443)
llm = OpenAI(temperature=0.1, model="gpt-4-1106-preview") #"gpt-4-1106-preview"


# Create QdrantVectorStore
vector_store = QdrantVectorStore(client=client, collection_name="alkohollagen_update2")
# Create the storage and service contexts
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(llm=llm)
# Build the VectorStoreIndex
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, service_context=service_context)
# Create a query engine and query
query_engine = index.as_query_engine(streaming = True, similarity_top_k=3)


# Streamlit UI
st.title("Fråga Falkenbergs Serveringstillståndsbot :robot_face:")
st.caption('Detta är en bot som hjälper till att besvara frågor kring serveringstillstånd. Den baserar sina svar från Folkhälsomyndigheten, alkohollagen och Falkenbergskommuns guide kring serveringstillstånd. Även om den kan en hel del så kan det ibland bli fel🙂')



user_input = st.text_input("**Vad söker svar på?** *(fråga på valfritt språk :flag-se::flag-eu::flag-gb::earth_africa::es::flag-fi::flag-sy:)")
if user_input:
    # Stream the GPT-4 reply
    response = query_engine.query(f"System instructions: Du hjälper användare att förstå information om serveringstillstånd i Falkenbergs kommun. Du inkluderar URL till de material du använder som kontext för ditt svar. svara så utförligt men enkelt som möjligt, gärna i punktform om det förbättrar svaret, User query: {user_input}. Du ger alltid källhänvisning till URL och du svarar alltid på samma språk som User query.")
    # with st.sidebar:
    #     for node in response.source_nodes:
    #         url = node.node.metadata['url']
    #         text = node.node.text
    #         score = node.score
    #         st.write(f"URL: {url}, Text: {text}, Score: {score}")
        # st.write(response.source_nodes)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in response.response_gen:

            full_response += chunk
            message_placeholder.markdown(full_response)
