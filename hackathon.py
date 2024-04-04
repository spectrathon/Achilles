import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd
import numpy as np
from app import main
import torch
import matplotlib.pyplot as plt

# Configure page layout
st.set_page_config(
    page_title="TruthGuard",
    page_icon=":speech_balloon:",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY_COLOR = "#566D7E"
PRIMARY_TEXT_COLOR = "#FFFFFF"

SECONDARY_COLOR = "#F7F7F7"
SECONDARY_TEXT_COLOR = "#333333"

ACCENT_COLOR = "#000000"
ACCENT_TEXT_COLOR = "#ffffff"


LARGE_FONT_SIZE = "24px"
MEDIUM_FONT_SIZE = "18px"
SMALL_FONT_SIZE = "14px"

USER_MESSAGE_COLOR = PRIMARY_COLOR
ASSISTANT_MESSAGE_COLOR = ACCENT_COLOR

USER_MESSAGE_STYLE = f"""
background-color: {USER_MESSAGE_COLOR};
color: {PRIMARY_TEXT_COLOR};
padding: 5px;
"""
ASSISTANT_MESSAGE_STYLE = f"""
background-color: {ASSISTANT_MESSAGE_COLOR};
color: {ACCENT_TEXT_COLOR};
padding: 10px;
"""

col1, col2 = st.columns(2)
col1.markdown(
    """
<div style="background-color:#000000; border: 2px solid black;color:#6F7780; border-radius: 10px; padding: 10px;">
<h3>Truth accuracy</h3>
<p>hitler was bad</p>
</div>
""",
    unsafe_allow_html=True,
)
col2.markdown(
    """
<div style="background-color:#000000;border: 2px solid black;color:#6F7780; border-radius: 10px; padding: 10px;">
<h3>Summarization</h3>
<p>Summarize this paragraph</p>
</div>
""",
    unsafe_allow_html=True,
)


st.title("TruthGuard")
st.divider()


st.sidebar.title("TruthGuard")
image_path = r"download.jpeg"
st.sidebar.image(image_path)
with st.sidebar.container():
    st.divider()
    st.header("Settings")
    user_name = st.text_input("Your Name", "User")
    show_timestamps = st.checkbox("Show Timestamps")
    st.divider()
    st.markdown(
        """
        <style>
.sidebar .element-container {
    background-color:#6F7780;
    padding: 10px;
    border-radius: 10px;
}
</style>
""",

        unsafe_allow_html=True,
    )


sidebar_chat_history = st.sidebar.container()
sidebar_chat_history.markdown(
 """  
<div style="background-color:#000000;border: 2px solid black;color:#6F7780; padding: 2px;">
<center><h3>History</h3><center>
</div>
""",
        unsafe_allow_html=True,

)


chat_history = []
input_container = st.container()

with input_container:
    cols = st.columns([10, 1])
    message_input = cols[0].text_input("**Welcome** " + user_name, key="message_input")
    cols[1].write("")
    cols[1].write("")
    send_button = cols[1].button("Send", use_container_width=True)

if send_button or (message_input and message_input[-1] == "\n"):
    if message_input:
        # Add user message to chat history
        chat_history.append(
            {
                "timestamp": datetime.now(),
                "name": user_name,
                "message": message_input,
                "is_user": True,
            }
        )

        # Display user message in sidebar chat history
        with sidebar_chat_history:
            st.markdown(
                f'<div style="background-color: {USER_MESSAGE_COLOR}; color: {PRIMARY_TEXT_COLOR}; padding: 5px; margin-bottom: 5px; border-radius: 5px;">{message_input}</div>',
                unsafe_allow_html=True,
            )

        # with open("C:/Users/91766/Desktop/CodeX/app.py", "a") as f:
        #     f.write(message_input)
    
    #m=open('a.txt')

    
    assistant_response,figure = main(message_input)

    # Add assistant message to chat history
    chat_history.append(
        {
            "timestamp": datetime.now(),
            "name": "Assistant",
            "message": assistant_response,
            "is_user": False,
        }
    )

    # Display assistant message in sidebar 
    with sidebar_chat_history:
        st.markdown(
            f'<div style="background-color: {ASSISTANT_MESSAGE_COLOR}; color: {ACCENT_TEXT_COLOR}; padding: 5px; margin-bottom: 10px; border-radius: 5px;">{assistant_response}</div>',
            unsafe_allow_html=True,
        )

   
    for chat in chat_history:
        if show_timestamps:
            st.write(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

        # Display user message
        if chat["is_user"]:
            st.markdown(
                f'<div style="{USER_MESSAGE_STYLE}">{chat["message"]}</div>',
                unsafe_allow_html=True,
            )
        # Display assistant message
        else:
            st.markdown(
                f'<div style="{ASSISTANT_MESSAGE_STYLE}">{chat["message"]}</div>',
                unsafe_allow_html=True,
            )
            with input_container:
                st.write(assistant_response)
                coln = st.columns([1, 1])
                torch.Tensor.ndim = property(lambda self: len(self.shape))
                plt.plot(figure)
                ch1=coln[0].plt.show()
                st.line_chart(ch1)

                # ch2=coln[1].


