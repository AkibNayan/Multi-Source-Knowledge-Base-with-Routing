from workflow import workflow
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

"""result = workflow.invoke({"query": "How do I authenticate API requests?"})

print("Original query:", result["query"])
print("\nClassifications:")
for c in result["classifications"]:
    print(f"  {c['source']}: {c['query']}")
print("\n" + "=" * 60 + "\n")
print("Final Answer:")
print(result["final_answer"])"""


import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# Create a ChatGroq instance
model = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api_key)


@tool
def search_knowledge_base(query: str) -> str:
    """Search across multiple knowledge sources (GitHub, Notion, Slack)

    Use this to find information about code, documentation,
    or team discusssions.
    """
    result = workflow.invoke({"query": query})
    return result["final_answer"]


conversational_agent = create_agent(
    model=model,
    tools=[search_knowledge_base],
    system_prompt=(
        "You are a helpful assistant that answers questions about our . "
        "Use the search_knowledge_base tool to find information across our "
        "code, documentation, and team discussions."
    ),
    checkpointer=InMemorySaver(),
)


config = {"configurable": {"thread_id": "user_123"}}

result = conversational_agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "How do I authenticate API requests?"}
        ],
    },
    config=config,
)

print(result["messages"][-1].content)

result = conversational_agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What about rate limiting for those endpoints?"}
        ],
    },
    config=config,
)

print(result["messages"][-1].content)
