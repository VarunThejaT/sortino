import streamlit as st
import requests
from streamlit_chat import message

# message("Interaction with Sortino:")

def setup_query_area():
    input_text = st.text_area(label="enter your query:", label_visibility='collapsed', placeholder="Your query...", key="query")
    return input_text

def query_llm(query):
    # return "testing"
    return query_berri_ai(query)

def query_berri_ai(query):
    """
    Attempt 1 - creating an instance of berri_ai_app for 
    querying the chunked data of a document.
    This can be extended to multiple documents. 
    Chunking strategy cannot be tweaked with.
    """
    url = "https://api.berri.ai/query"

    querystring = {
        "user_email": "varuntheja.atp@gmail.com",
        "instance_id": "6712b60f-28b7-471d-8af5-202d96b8a522",
        "query": query,
        "model": "gpt-3.5-turbo"
    }
    response = requests.get(url, params=querystring)
    
    if response.status_code != 200:
        print(response.json())    
        return "hmm, something went wrong with querying the response"

    return response.json()["response"]

def process_query():
    query = st.session_state["query"]
    if len(query.split(" ")) > 700:
        st.write("Please enter a shorter query. The maximum length is 700 words.")
        st.stop()
    st.session_state["chat_history"].append((query, True)) #user is True

    response_from_llm = query_llm(query)
    st.session_state["chat_history"].append((response_from_llm, False)) # user is False
    # clear the input in the text_area
    st.session_state["query"] = ""

def print_chat():
    for idx, (msg, usr) in enumerate(st.session_state.chat_history):
        # key is necessary to keep the chats unique and the chat from blowing up
        message(msg, is_user=usr, key=str(idx))

def setup_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "option_source_sec" not in st.session_state:
        st.session_state.option_source_sec = False

def setup_heading():
    st.set_page_config(page_title="Sortino", page_icon=":robot:")
    st.header("Sortino")

def setup_input_options():
    col1, col2 = st.columns(2)
    with col1:
        # choose the company - this should be a pretty quick lookup of all the options available
        # for demo purposes, we would have just one drop down
        option_company = st.selectbox( 'Company?', ['Meta'])

    with col2:
        # choose the source 
        st.markdown('Source:')
        # option_source = st.radio('Sources:', ['News'])
        st.checkbox('SEC', key="option_source_sec")

def main():
    setup_session_state()

    setup_heading()

    setup_input_options()
    
    print_chat()

    setup_query_area()

    st.button("send", on_click=process_query)

if __name__ == "__main__":
    main()