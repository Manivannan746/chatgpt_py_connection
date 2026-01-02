from google.adk.agents import Agent

third_party_assistant = Agent(
    name="Search_flights",
    model="gemini-2.5-flash",
    description="Flight Assistance AI",
    instruction="""You are a friendly assistant
    1, Greet the user
    2, Get Departure and arrival date from user
    3, From to To location
    4, Preference like Business, economy
    5, Select the lowest flight and checkout""",
)

# This is the variable the ADK loader looks for
root_agent = third_party_assistant