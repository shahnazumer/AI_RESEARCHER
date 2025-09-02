# Step1: Define state
from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the state schema using TypedDict
# 'messages' will hold a list of conversation messages, and Annotated ensures
# messages can be updated with add_messages logic
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Step2: Define ToolNode & Tools
from arxiv_tool import *   # Tool for searching research papers from arxiv.org
from read_pdf import *     # Tool for reading content from PDF files
from write_pdf import *    # Tool for rendering LaTeX into PDF
from langgraph.prebuilt import ToolNode

# Collect tools into a list for the agent to use
tools = [arxiv_search, read_pdf, render_latex_pdf]

# ToolNode wraps the tools so they can be invoked in the workflow
tool_node = ToolNode(tools)


# Step3: Setup LLM
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Google Generative AI model (Gemini 2.5 Pro) with API key from env
# Bind the tools so model can call them directly during reasoning
model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", api_key=os.getenv("GOOGLE_API_KEY")).bind_tools(tools)
model = model.bind_tools(tools)


# Step4: Setup graph
#from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph

# Function to call the LLM with conversation state
def call_model(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}  # Return new response as messages


# Decide whether the workflow should continue to tools or end
def should_continue(state: State) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    # If the last message requires tool execution, go to tools
    if last_message.tool_calls:
        return "tools"
    return END  # Otherwise, end workflow

# Build the graph workflow
workflow = StateGraph(State)
workflow.add_node("agent", call_model)      # Agent node runs the model
workflow.add_node("tools", tool_node)       # Tools node executes external tools
workflow.add_edge(START, "agent")           # Start → Agent
workflow.add_conditional_edges("agent", should_continue)  # Agent → Tools or End
workflow.add_edge("tools", "agent")         # After tools, return back to agent

# Add checkpointing to save memory of conversation
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
config = {"configurable": {"thread_id": 222222}}  # Custom thread ID

# Compile graph with checkpointer
graph = workflow.compile(checkpointer=checkpointer)


# Step5: TESTING
# System prompt that defines how the agent should behave
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

# Function to print responses as they stream from the graph
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(f"Message received: {message.content[:200]}...")  # Print preview of response
        message.pretty_print()  # Pretty-print the full message


# Uncomment this block for interactive testing in terminal
"""
while True:
    user_input = input("User: ")
    if user_input:
        messages = [
                    {"role": "system", "content": INITIAL_PROMPT},
                    {"role": "user", "content": user_input}
                ]
        input_data = {
            "messages" : messages
        }
        print_stream(graph.stream(input_data, config, stream_mode="values"))
"""
