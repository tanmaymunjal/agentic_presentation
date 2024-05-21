from langchain.agents import Tool
from langchain_community.tools.google_jobs import GoogleJobsQueryRun
from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
import os
from config import global_config

os.environ["SERPAPI_API_KEY"] = global_config["AUTH"]["SERP_API_KEY"]
os.environ["OPENAI_API_KEY"] = global_config["AUTH"]["OPENAI_API_KEY"]

model = ChatOpenAI(model="gpt-3.5-turbo")
search = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())
tools = [
    Tool(
        name="Google_job_search",
        func=search.run,
        description="useful for when you need info regarding jobs",
    )
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant for helping people apply to jobs.
            Make sure to include the minimum number of jobs specified.
            Make sure to assume no additional qualitfication that is not mentioned in description.
            Assume that they do not want to downgrade their prestige from past experience.""",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


def invoke_agent_google_jobs(indv_desc: str, k: int = 5) -> str:
    message = agent_executor.invoke(
        {"input": f"Find the {k} best jobs for the individual \n {indv_desc}."}
    )
    return message["output"]