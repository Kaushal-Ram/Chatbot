from langchain_groq import ChatGroq
import os
import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
import warnings
#from langchain_core.chat_history import (
 #   BaseChatMessageHistory,
  #  InMemoryChatMessageHistory,)
#from langchain_core.runnables.history import RunnableWithMessageHistory
#from operator import itemgetter
#from langchain_core.runnables import RunnablePassthrough

warnings.simplefilter(action='ignore', category=FutureWarning)

st.title("Chatbot")

os.environ['TOKENIZERS_PARALLELISM'] = "False"

st.session_state["models"] = {'Gemma 2 9B':'gemma2-9b-it','Gemma 7B':'gemma-7b-it',
                              'Meta Llama 3 70B':'llama3-70b-8192','Meta Llama 3 8B':'llama3-8b-8192'}

st.session_state["model"] = ChatGroq(model = st.session_state["models"]['Gemma 2 9B'])
st.session_state["prompt"] = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant. Answer the asked questions to the best of your ability"), 
        MessagesPlaceholder(variable_name="messages")]
    )
st.session_state["chain"] = st.session_state["prompt"]|st.session_state["model"]

def change_model():
    st.session_state["model"] = ChatGroq(model = st.session_state["models"][st.session_state["selected_model"]])
    st.session_state["chain"] = st.session_state["prompt"]|st.session_state["model"]

model_selected = st.selectbox("Choose a model", list(st.session_state["models"].keys()), key = "selected_model")

#print(st.session_state["selected_model"])
#model = ChatGroq(model=str(models['Meta Llama 3 8B']))

#store = {}


#def get_session_history(session_id: str) -> BaseChatMessageHistory:
#    if session_id not in store:
#        store[session_id] = InMemoryChatMessageHistory()
#    return store[session_id]

#trimmer = trim_messages(
 #   max_tokens=2000,
  #  strategy="last",
  #  token_counter=model,
   # include_system=True,
  #  allow_partial=False,
   # start_on="human",
    #)

#(RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer))
#chain = prompt|model

#with_message_history = RunnableWithMessageHistory(
 #   chain,
  #  get_session_history,
   # input_messages_key="messages",
    #)


#config = {"configurable": {"session_id": "0001"}}


def chat_actions():
     st.session_state["chat_history"].append({'role':'you', 'content':st.session_state["msg_in"]})
     st.session_state["messages"].append(HumanMessage(content = st.session_state["msg_in"]))
     st.session_state["model"] = ChatGroq(model = st.session_state["models"][st.session_state["selected_model"]])
     st.session_state["chain"] = st.session_state["prompt"]|st.session_state["model"]
     response = st.session_state["chain"].invoke(
            {
                "messages": st.session_state["messages"],
            }
            )
     st.session_state["chat_history"].append({'role':'chatbot', 'content':response.content})
     st.session_state["messages"].append(AIMessage(content = response.content))
     #if len(st.session_state["chat_history"]) > 20:
      #    st.session_state["chat_history"] = st.session_state["chat_history"][-20:]
       #   st.session_state["messages"] = st.session_state["messages"][-20:]


msg_input = st.chat_input("Type your message", key = "msg_in", on_submit = chat_actions)

        
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state["messages"] = []

for i in st.session_state["chat_history"]:
     with st.chat_message(i['role']):
          st.write(i['content'])


