import streamlit as st
import pandas as pd
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.core import ServiceContext
from llama_index.core.query_engine import RetrieverQueryEngine

# Set page title
st.set_page_config(page_title="Netflix Chatbot", layout="wide")
st.title("🎬 Netflix CSV Chatbot (Powered by Ollama)")

# Load and show CSV
@st.cache_data
def load_csv():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_csv()
st.dataframe(df.head(10))

# Load Ollama LLM
llm = Ollama(model="llama3")  # you can use "mistral" or others

# Prepare documents from CSV
@st.cache_resource
def load_index():
    documents = SimpleDirectoryReader(input_files=["netflix_titles.csv"]).load_data()
    service_context = ServiceContext.from_defaults(llm=llm)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    return index

index = load_index()
query_engine = index.as_query_engine()

# Chat UI
st.subheader("Ask something about Netflix data 👇")
user_input = st.text_input("Type your question...")

if user_input:
    with st.spinner("Thinking..."):
        response = query_engine.query(user_input)
        st.success(response.response)
