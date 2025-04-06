import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()


class WeatherAgent:
    def __init__(self, server_path: str):
        """Initialize the Weather Agent with the path to the weather server."""
        self.server_path = os.path.abspath(server_path)
        self.client = None
        self.agent = None

    async def initialize(self):
        """Initialize the MCP client and create the agent."""
        server_config = {
            "weather": {
                "command": "python",
                "args": [self.server_path],
                "transport": "stdio",
            },
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv(
                        "GITHUB_PERSONAL_ACCESS_TOKEN"
                    )
                },
            },
        }

        self.client = MultiServerMCPClient(server_config)
        await self.client.__aenter__()

        # Create the agent with the tools
        llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
        self.agent = create_react_agent(llm, self.client.get_tools())

    async def query(self, question: str) -> str:
        """Query the weather agent with a natural language question."""
        if not self.agent:
            await self.initialize()

        try:
            response = await self.agent.ainvoke(
                {"messages": [{"role": "user", "content": question}]}
            )

            # Handle different response types
            if isinstance(response, AIMessage):
                return response.content
            elif isinstance(response, dict):
                if "messages" in response:
                    return response["messages"][-1].content
                elif "output" in response:
                    return response["output"]
            return str(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"

    async def close(self):
        """Close the MCP client connection."""
        if self.client:
            await self.client.__aexit__(None, None, None)
