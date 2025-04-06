from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from mcp.adapters.langchain import MCPToolAdapter
from mcp.client import MCPClient

# Load environment variables
load_dotenv()


class WeatherAgent:
    def __init__(self, server_path: str):
        """Initialize the Weather Agent with the path to the weather server."""
        self.client = MCPClient(server_path)
        self.tools = MCPToolAdapter(self.client).get_tools()
        self.agent = self._create_agent()

    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent with OpenAI functions."""
        llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful weather assistant that can provide weather information using the available tools.
            When asked about weather:
            1. For state-wide alerts, use the get_alerts tool with the state code
            2. For location-specific forecasts, use the get_forecast tool with latitude,longitude
            3. Always provide clear, concise responses
            4. If you need coordinates for a city, use your knowledge to provide them
            """,
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_openai_functions_agent(llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def query(self, question: str) -> str:
        """Query the weather agent with a natural language question."""
        return self.agent.invoke({"input": question})["output"]
