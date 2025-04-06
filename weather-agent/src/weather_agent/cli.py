import argparse
import asyncio

from .agent import WeatherAgent


async def main_async():
    parser = argparse.ArgumentParser(description="Weather Agent CLI")
    parser.add_argument(
        "--server",
        default="../weather-server-python/weather.py",
        help="Path to the weather server script",
    )
    args = parser.parse_args()

    print("Initializing Weather Agent...")
    agent = WeatherAgent(args.server)
    await agent.initialize()

    print("\nWeather Agent is ready! Type 'quit' to exit.")
    print("Example questions:")
    print("- What are the current weather alerts in California?")
    print("- What's the forecast for San Francisco?")
    print("- Are there any weather alerts in New York?")
    print()

    try:
        while True:
            question = input("Question: ").strip()
            if question.lower() == "quit":
                break
            if not question:
                continue

            response = await agent.query(question)
            print("\nResponse:", response, "\n")
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await agent.close()


def main():
    """Entry point for the CLI."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
