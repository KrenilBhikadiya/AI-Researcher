import streamlit as st
from langgraph_agent import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄")
st.title("📄 Research AI Agent")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# Chat interface
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # Log and display user input
    logger.info(f"User input: {user_input}")
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Stream agent response
    full_response = ""
    
    # Prepare messages: include system prompt only on first message
    if len(st.session_state.chat_history) == 1:
        # First message: include system prompt
        messages = [
            SystemMessage(content=INITIAL_PROMPT),
            HumanMessage(content=user_input)
        ]
    else:
        # Subsequent messages: only send current user input
        messages = [HumanMessage(content=user_input)]
    
    for s in graph.stream(
        {"messages": messages},
        config={"configurable": config},
        stream_mode="values",
    ):
        message = s["messages"][-1]

        # Handle tool calls (log only)
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                logger.info(f"Tool call: {tool_call['name']}")

        # Handle assistant response
        if isinstance(message, AIMessage) and message.content:
            text_content = (
                message.content
                if isinstance(message.content, str)
                else str(message.content)
            )
            full_response += text_content + " "
            st.chat_message("assistant").write(full_response)

    # Add final response to history
    if full_response:
        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response}
        )
