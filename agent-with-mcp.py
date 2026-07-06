import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from dotenv import load_dotenv

load_dotenv()


async def run(question: str):

    client = MultiServerMCPClient(
        {
            "okf": {
                "transport": "streamable_http",
                "url": "http://localhost:8000/mcp",
            }
        }
    )
    tools = await client.get_tools()

    system_prompt = (
        "You are an assistant answering questions using an OKF knowledge "
        "bundle. Start with okf_list_concepts or okf_find_by_type/tag to "
        "orient yourself, then okf_read_concept to pull in only the "
        "concepts you actually need, following okf_get_links to traverse "
        "related concepts. Don't read the whole bundle up front."
    )

    agent = create_agent(
        model="gpt-5.4-mini",
        tools=tools,
        system_prompt=system_prompt,
    )

    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":

    question = "What front-end framework should I use"
    asyncio.run(run(question))
