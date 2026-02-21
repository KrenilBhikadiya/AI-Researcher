import os
from dotenv import load_dotenv
from pdf_reader import read_pdf
from pdf_writer import render_latex_pdf
from arxiv_tool import arxiv_tool
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent


load_dotenv()

model = ChatAnthropic(
    model_name=os.getenv("CLAUDE_MODEL", "claude-2"),
    timeout=None,
    stop=None
)

graph = create_agent(model=model, tools=[read_pdf, render_latex_pdf, arxiv_tool])

def print_stream(stream):
    for item in stream:
        message = item["messages"][-1]  # Get the last message in the stream
        print("Message Received: ", message.content[:200])
        message.pretty_print()  # Pretty print the message content

while True:
    user_input = input("User: ")
    if user_input:
        print_stream(graph.stream(
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            }, 
            stream_mode="values"
        ))