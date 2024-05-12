from langchain.agents import Tool
from langchain_community.utilities import SearchApiAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
import os
from config import global_config

os.environ["SEARCHAPI_API_KEY"] = global_config["AUTH"]["SEARCHAPI_API_KEY"]
os.environ["OPENAI_API_KEY"] = global_config["AUTH"]["OPENAI_API_KEY"]

model = ChatOpenAI(model="gpt-3.5-turbo")
search = SearchApiAPIWrapper()
tools = [
    Tool(
        name="Google_search",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant for creating detailed corporate reports. 
            Make sure to use the Google_search tool for information.
            Do not ask follow up questions, generate the report to best of your ability""",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


def invoke_agent(ques: str):
    message = agent_executor.invoke(
        {"input": f"Write a detailed report on {ques} in 1000 words."}
    )
    return message["output"]
