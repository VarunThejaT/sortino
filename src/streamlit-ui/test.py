import streamlit as st

def main():
    st.title("Streamlit Chat")

    # Create a persistent state to store the chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Input field for the user to enter their message
    user_input = st.text_input("Enter your message:", value="", key=1)

    # Button to send the message
    if st.button("Send"):
        # Append the user's message to the chat history
        st.session_state.chat_history.append(("You", user_input))

        # Simulate a response from the chatbot (you can replace this with your own logic)
        response = "Hello, I am a chatbot. You said: " + user_input
        st.session_state.chat_history.append(("Chatbot", response))


    # Define custom CSS for the chat container
    chat_container_css = """
    <style>
        .chatcontainer {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
    """

    # Render the custom CSS
    st.markdown(chat_container_css, unsafe_allow_html=True)

    # # Create a container for the chat messages
    # with st.container():
    #     # Apply the custom CSS class to the container
    #     st.markdown(chat_container_css, unsafe_allow_html=True)
    #     st.markdown('<div class="chatcontainer">', unsafe_allow_html=True)

    #     # Display the chat history inside the container
    #     for sender, message in st.session_state.chat_history:
    #         st.markdown(f"<b>{sender}:</b> {message}<br>", unsafe_allow_html=True)

    #     st.markdown('</div>', unsafe_allow_html=True)
    
    my_div = st.container()
    with my_div:
        conversation = []
        for sender, message in st.session_state.chat_history:
            conversation.append(f"<b>{sender}:</b> {message}<br>")
        total_conversation = "".join(conversation)
        my_div.markdown(f'<div class="chatcontainer"/> {total_conversation} </div>', unsafe_allow_html=True)
        # my_div.with_attrs({"class": "chat-container"})
        
if __name__ == "__main__":
    main()
