# Step1: Install & Import dependencies
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from arxiv_tool import arxiv_search
from read_pdf import read_pdf
from write_pdf import render_latex_pdf
import os
from dotenv import load_dotenv

load_dotenv()

# Step2: Setup LLM and tools
tools = [arxiv_search, read_pdf, render_latex_pdf]
model = ChatGoogleGenerativeAI(model="gemini-2.5-pro", api_key=os.getenv("GOOGLE_API_KEY"))

# Step3: Create the ReAct agent graph
graph = create_react_agent(model, tools=tools)

# Step4: Run the agent with an initial prompt

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
render it as a LaTeX PDF. When you give papers references, always attatch the pdf links to the paper"""


# Define a helper function to print messages from the stream
def print_stream(stream):
    # Loop through each item in the stream
    for s in stream:
        # Extract the last message from the "messages" list
        message = s["messages"][-1]

        # Print first 200 characters of the message content (preview)
        print(f"Message received: {message.content[:200]}...")

        # Use the built-in pretty_print() method to display the full formatted message
        message.pretty_print()


# Main interaction loop (runs continuously until interrupted)
while True:
    # Take user input from the console
    user_input = input("User: ")

    # Proceed only if the user entered some text
    if user_input:
        # Construct conversation history with system and user roles
        messages = [
                    {"role": "system", "content": INITIAL_PROMPT},  # System instruction/prompt
                    {"role": "user", "content": user_input}         # User's current input
                ]

        # Wrap messages in an input data object
        input_data = {
            "messages" : messages
        }

        # Stream responses from the graph and print them using print_stream()
        print_stream(graph.stream(input_data, stream_mode="values"))
