## works with CGPT
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import pinecone
import os
from dotenv import load_dotenv

load_dotenv()
OPENkey = os.environ.get('OPENAI_API_KEY')
Pinecone_key = os.environ.get('Pinecone_API')
Pinecone_env = os.environ.get('Pinecone_Environment')

# def main():
st.set_page_config(page_title="Archer's Arena")
st.header("ArrowBot: Your Archery Assistant 🏹")


input_text = st.text_input("Curiosity killed the cat, but it won't harm you! Ask us anything!", placeholder="Type your question and press enter")


def generate_response():
    query = input_text
    embeddings = OpenAIEmbeddings(openai_api_key=OPENkey)

    # initialize connection to pinecone
    pinecone.init(
      api_key=Pinecone_key,
      environment=Pinecone_env
    )

    # point to my index
    index_name = 'aa-index'
    # connect to the index
    pinecone_index = pinecone.Index(index_name)
    
    # load existing index
    docsearch = Pinecone.from_existing_index(index_name, embeddings, namespace="archers-sop")
    data = docsearch.similarity_search(query, k=3)

    llm = OpenAI(temperature=0.7, openai_api_key=OPENkey)
    chain = load_qa_chain(llm, chain_type="map_reduce")
    res = chain({"input_documents": data, "question": query})
    return res.get('output_text')

if input_text:
    output = generate_response()
    st.write(output)
