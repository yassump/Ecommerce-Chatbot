import os
from google import genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
print(api_key)
# Initialize client once in session_state
if "client" not in st.session_state:
    st.session_state.client=genai.Client()
client=st.session_state.client
system_prompt="""you are an AI assistant designed only for ecommerce and shopping support.
your job is to help the users with
- Finding the products
- comparing the products
- suggesting products based on budget,needs
- Explaining Features
- Recommending products
keep responses short and practical
if the question is not related to ecommerce just say iam only trained on ecommerce assistance cant help with this question.
Keep answers clear,helpful,focused on buying decessions.'.
you may respond to simple greetings like:hello,hi,thanks... 
if you are asking for budget range must be in indian rupees.
Ask the follow up questions if needed.
Never answer to non ecommerce related question if you have doubt whether it is ecommerce or not simply reply iam only trained on ecommerce"""
st.title("your smart Shopping Assistant")
st.markdown("""
Try asking:
    - Suggest Laptop under budget
    - Best mobile for gaming
    - Budget headphones""")
# initialize chat session only once
if "chat_session" not in st.session_state:
    st.session_state.chat_session=client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(system_instruction=system_prompt)
    )
if "messages" not in st.session_state:
    st.session_state.messages=[]
print(st.session_state)
#Display past messages
for role,text in st.session_state.messages:
    if role=="user":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Bot:** {text}")
# caht input
user_input=st.chat_input("What would you like to buy today?")
if user_input:
    st.session_state.messages.append(("user",user_input))
    chat=st.session_state.chat_session
    response=chat.send_message(user_input)
    bot_reply=response.text
    st.session_state.messages.append(("bot",bot_reply))
    st.rerun()