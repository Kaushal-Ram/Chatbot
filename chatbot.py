from langchain_groq import ChatGroq
import os
import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

os.environ['TOKENIZERS_PARALLELISM'] = "False"

st.session_state["models"] = {'Gemma 2 9B':'gemma2-9b-it','Gemma 7B':'gemma-7b-it',
                              'Meta Llama 3 70B':'llama3-70b-8192','Meta Llama 3 8B':'llama3-8b-8192'}

def clear_chat():
     st.session_state["messages"] = []

with st.sidebar:
    st.title("Chatbot")
    model_selected = st.selectbox("Choose a model", list(st.session_state["models"].keys()), key = "selected_model")
    clear_chat_button = st.button("Clear chat", on_click = clear_chat)

st.session_state["model"] = ChatGroq(model = st.session_state["models"]['Gemma 2 9B'])
st.session_state["prompt"] = ChatPromptTemplate.from_messages(
        [("system", '''You are a helpful assistant. Answer the user's questions to the 
          best of your ability'''), 
        MessagesPlaceholder(variable_name="messages")]
    )
st.session_state["chain"] = st.session_state["prompt"]|st.session_state["model"]

def chat_actions():
     st.session_state["messages"].append(HumanMessage(content = st.session_state["msg_in"]))
     st.session_state["model"] = ChatGroq(model = st.session_state["models"][st.session_state["selected_model"]])
     st.session_state["chain"] = st.session_state["prompt"]|st.session_state["model"]
     response = st.session_state["chain"].invoke(
            {
                "messages": st.session_state["messages"],
            }
            )
     st.session_state["messages"].append(AIMessage(content = response.content))
     if len(st.session_state["messages"]) > 20:
          st.session_state["messages"] = st.session_state["messages"][-20:]

msg_input = st.chat_input("Type your message", key = "msg_in", on_submit = chat_actions)
        
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for i in st.session_state["messages"]:
     with st.chat_message(i.type):
          st.write(i.content)
