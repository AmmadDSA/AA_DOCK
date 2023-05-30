import os
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import openai
import pinecone
from dotenv import load_dotenv
load_dotenv()

## call key by os.environ.get || or by os.getenv **remember to restart kernel if changes were made
OPEN_KEY = os.environ.get('OPENAI_API_KEY')
Pinecone_key = os.environ.get('Pinecone_API')
Pinecone_environ = os.getenv('Pinecone_Environment')
# print(OPEN_KEY)
st.set_page_config(page_title="Archers Arena")
st.header("Arrow Mcbot: Your Email Assistant 👩‍💻")

# prompt = st.text_input(label="Ask away",placeholder="paste email body and press enter")
prompt = "what is the price for beginners archery"


def generate_email_reply(prompt):
    # pass the email query
    query_em = prompt

    # define embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_KEY)

    # initialize connection to pinecone
    pinecone.init(api_key=Pinecone_key, environment=Pinecone_environ)
    
    # connect to the index
    index_name = 'aa-index'
    pinecone_index = pinecone.Index(index_name)
    docsearch = Pinecone.from_existing_index(index_name, embeddings, namespace="archers-sop")

    # query_em = """We are looking to book a group of about 20-25 youth. Could you please tell me if you have availability for these dates and what are some of the activities?"""
    data_em = docsearch.similarity_search(query_em, k=2)

    # question_prompt_template = """Use the following documents to see if any of the text is relevant to answer the question. 
    # Return any relevant text.

    ## Email Template
    question_prompt_template = """Use the context documents to create an email reply
    {context}
    Question: {question}
    Answer in an email format"""
    QUESTION_PROMPT = PromptTemplate(template=question_prompt_template, input_variables=["context", "question"])

    combine_prompt_template = """create a final answer as an email. 
    If you don't know the answer, just say that you will need to ask the manager and get back to them. Don't try to make up an answer.
    QUESTION: {question}
    =========
    {summaries}
    =========
    Always add this as a prefix in bullets:  \n\nEntry depends on:\n• How many people you bring\n• How long you want to play\n• How many activities\n\nOur pricing is:\n• 1h, 1 activity = \$45 per person (tax inc)\n• 2h, 2 activities = \$65 per person (tax inc)\n• 2h, 3 activities = \$75 per person (tax inc)\n\nOur private activities are:\n• Combat Archery (like dodgeball with bows and arrows)\n• Nerf Blaster Battles\n• Lightsaber Battles\n• Bubble Soccer\n• Black Light Dodgeball/Basketball \n
    Always add this as a suffix: \n\nAll sessions are facilitated by a coach.\nMinimum 12 people group. 20 people maximum in one court, but if have more - go up to the 2nd court (if it's available) or do teams and rotations.\nCredit card details are only needed reserve the booking (Not Charged) the actual payement is completed afterwards, decided by your group.\nI would advise you to book asap because we are a first-come-first-serve basis!\nIf you have any questions, please reply back and I'll respond as soon as possible!
    Answer in an email format:"""
    COMBINE_PROMPT = PromptTemplate(template=combine_prompt_template, input_variables=["summaries", "question"])

    chain = load_qa_chain(OpenAI(temperature=0.6, openai_api_key=OPEN_KEY), chain_type="map_reduce", return_map_steps=True, question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)
    # chain = load_qa_chain(llm=OpenAI(temperature=0.3), chain_type="map_reduce", return_map_steps=True, question_prompt=QUESTION_PROMPT)
    res =chain({"input_documents": data_em, "question": query_em}, return_only_outputs=True)

    return(res.get('output_text'))


if prompt:
    reply = generate_email_reply(prompt)
    container = st.container()
    container.write(reply)



# #   You can now view your Streamlit app in your browser.
# # Local URL: http://localhost:8501
# # Network URL: http://192.168.1.99:8501