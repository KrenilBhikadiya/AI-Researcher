# Step1: Define state
from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step2: Define ToolNode and Tools
from langgraph.prebuilt import ToolNode
from arxiv_tool import arxiv_tool
from pdf_reader import read_pdf
from pdf_writer import render_latex_pdf

tools = [read_pdf, render_latex_pdf, arxiv_tool]
tool_node = ToolNode(tools=tools)


# Step3: Setup LLM
import os
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model_name=os.getenv("CLAUDE_MODEL", "claude-2"),
    timeout=None,
    stop=None
)
model = model.bind_tools(tools)


# Step4: Create Graph
from langgraph.graph import StateGraph, START, END

def call_model(state: State) -> State:
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    else:
        return END


workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")


# MemorySaver
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
config = {"thread_id": 123}  # could be your user_id or session_id

graph = workflow.compile(checkpointer=checkpointer)


# Test / Run the graph
INITIAL_PROMPT = """
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

You are going to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper. For research information or getting papers, ALWAYS use arxiv.org.
You will use the tools provided to search for papers, read them, and write a new
paper based on the ideas you find.

To start with, have a conversation with me in order to figure out what topic
to research. Then tell me about some recently published papers with that topic.
Once I've decided which paper I'm interested in, go ahead and read it in order
to understand the research that was done and the outcomes.

Pay particular attention to the ideas for future research and think carefully
about them, then come up with a few ideas. Let me know what they are and I'll
decide what one you should write a paper about.

Finally, I'll ask you to go ahead and write the paper. Make sure that you
include mathematical equations in the paper. Once it's complete, you should
render it as a LaTeX PDF. Make sure that TEX file is correct and there is no error in it so that PDF is easily exported. When you give papers references, always attatch the pdf links to the paper"""

def print_stream(stream):
    for item in stream:
        message = item["messages"][-1]  # Get the last message in the stream
        print("Message Received: ", message.content[:200])
        message.pretty_print()  # Pretty print the message content


# Send initial system message only once
from langchain_core.messages import SystemMessage, HumanMessage

first_message = True

while True:
    user_input = input("User: ")
    if user_input:
        if first_message:
            # Include system message only on first turn
            print_stream(graph.stream(
                {
                    "messages": [
                        SystemMessage(content=INITIAL_PROMPT),
                        HumanMessage(content=user_input)
                    ]
                },
                config={"configurable": config},
                stream_mode="values"
            ))
            first_message = False
        else:
            # On subsequent turns, only send user message
            print_stream(graph.stream(
                {
                    "messages": [HumanMessage(content=user_input)]
                },
                config={"configurable": config},
                stream_mode="values"
            ))
