import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv ()
llm = ChatGoogleGenerativeAI ( model="gemini-1.5-flash" )

qa_system_prompt = """You are a helpful AI assistant. Your goal is to provide accurate and relevant answers based on the user's latest question and the previous chat history. 

1. Carefully consider the context provided in the chat history.
2. Respond to the user's query in a clear and concise manner.
3. If the user's question is unclear or lacks sufficient context, ask for clarification rather than making assumptions.
4. Maintain a friendly and engaging tone throughout the conversation.
"""

qa_prompt = ChatPromptTemplate.from_messages ( [
    ("system", qa_system_prompt),
    MessagesPlaceholder ( "chat_history" ),
    ("human", "{input}"),
] )

final_chain = (qa_prompt | llm)

# Streamlit UI
st.title ( "AI Chat Assistant" )

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Input box for user query
user_input = st.text_input ( "You:", "" )

if st.button ( "Send" ):
    if user_input:
        # Invoke the AI model
        result = final_chain.invoke ( {"input": user_input, "chat_history": st.session_state.chat_history} )

        # Display AI response
        # st.text ( f"AI: {result.content}" )

        # Display AI response with improved styling
        st.markdown (
            f"<div style='max-width: 800px; padding: 10px; border-radius: 5px; background-color: #0000; border: 1px solid #d1d1d6;'>{result.content}</div>",
            unsafe_allow_html=True )

        # Update chat history
        st.session_state.chat_history.append ( HumanMessage ( content=user_input ) )
        st.session_state.chat_history.append ( AIMessage ( content=result.content ) )
    else:
        st.warning ( "Please enter a message." )


# # Display chat history this code will display the chat hisotry as well in the ui
# if st.session_state.chat_history:
#     st.subheader ( "Chat History:" )
#     for message in st.session_state.chat_history:
#         if isinstance ( message, HumanMessage ):
#             st.text ( f"You: {message.content}" )
#         else:
#             st.text ( f"AI: {message.content}" )