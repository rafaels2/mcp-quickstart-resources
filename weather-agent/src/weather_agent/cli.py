import argparse

from .agent import WeatherAgent


def main():
    parser = argparse.ArgumentParser(description="Weather Agent CLI")
    parser.add_argument(
        "--server",
        default="../weather-server-python/weather.py",
        help="Path to the weather server script",
    )
    args = parser.parse_args()

    print("Initializing Weather Agent...")
    agent = WeatherAgent(args.server)
    print("\nWeather Agent is ready! Type 'quit' to exit.")
    print("Example questions:")
    print("- What are the current weather alerts in California?")
    print("- What's the forecast for San Francisco?")
    print("- Are there any weather alerts in New York?")
    print()

    while True:
        try:
            question = input("Question: ").strip()
            if question.lower() == "quit":
                break
            if not question:
                continue

            response = agent.query(question)
            print("\nResponse:", response, "\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()
