from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import streamlit as st
import base64

st.set_page_config(page_title='ServeringsChat', page_icon="🤖")

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# URL to be linked
url = "https://www.example.com"

# Path to your image
image_path = "image2.png"

# Get the base64 string of the image
image_base64 = get_image_base64(image_path)

# HTML code to make the image clickable
html = f"""
    <a href="{url}" target="_blank">
        <img src="data:image/png;base64,{image_base64}" alt="Clickable image" style="width: 30%; height: auto;">
    </a>
"""


st.markdown(html, unsafe_allow_html=True)

@st.cache_data
def convert_bg_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = convert_bg_as_base64("background.png")

page_bg_img = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{

background-image: url("data:image/png;base64,{img}");
background-position: center;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Replace this URL with the actual URL you want to link to
link = 'https://falkenberg.infocaption.com/players/outlineplayer/print/CreateOutlineHTMLForPrinting.jsp?GuideID=1289&rootNodeIndex=0'
link_text = 'Klicka här för att läsa en summerande text om serveringstillstånd i Falkenbergskommun' #:linked_paperclips: 

# HTML with inline CSS for styling
html_link = f'''
    <a href="{link}" target="_blank">
        <button style="
            background-color: #5de3d3; /* Pastel Pink #FFC0CB */
            border: none;
            color: grey;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 15px !important; /* Rounded corners */
            box-shadow: 3px 3px 5px grey; /* Drop shadow */
        ">{link_text}</button>
    </a>
'''

st.markdown(html_link, unsafe_allow_html=True)



# Set up the Qdrant client
url = 'qdrant.utvecklingfalkenberg.se'
api_key = st.secrets["QDRANT_API_KEY"]
client = QdrantClient(url=url, api_key=api_key, port=443)
llm = OpenAI(temperature=0.1, model="gpt-4-1106-preview") #"gpt-4-1106-preview"


# Create QdrantVectorStore
vector_store = QdrantVectorStore(client=client, collection_name="alkohollagen_update3")
# Create the storage and service contexts
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(llm=llm)
# Build the VectorStoreIndex
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, service_context=service_context)
# Create a query engine and query
query_engine = index.as_query_engine(streaming = True, similarity_top_k=3)


# Streamlit UI
st.title("Fråga Falkenbergs Serveringstillståndsbot :robot_face:")
st.caption('Detta är en bot som hjälper till att besvara frågor kring serveringstillstånd. Den baserar sina svar från Folkhälsomyndigheten, alkohollagen och Falkenbergskommuns guide kring serveringstillstånd. Även om den kan en hel del, så kan det ibland bli fel🙂 Du kan också öva med våra Quizar till vänster som erbjuds på Svenska, Engelska och Arabiska')


# Query and response code:
user_input = st.text_input("**Vad söker du svar på?** *(fråga på valfritt språk :flag-se::flag-eu::flag-gb::earth_africa::es::flag-fi::flag-sy:)")
if user_input:
    # Stream the GPT-4 reply
    response = query_engine.query(f"System instructions: Du hjälper användare att förstå information om serveringstillstånd i Falkenbergskommun. Du inkluderar URL till de material du använder som kontext för ditt svar. svara så utförligt men enkelt som möjligt, gärna i punktform om det förbättrar svaret, User query: {user_input}. Du ger alltid källhänvisning till URL och du svarar alltid på samma språk som User query.")
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
