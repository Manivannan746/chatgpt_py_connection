import os
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def ask_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env file")
    else:
        user_prompt = input("Enter your prompt: ")
        answer = ask_chatgpt(user_prompt)
        print("\nChatGPT Response:\n")
        print(answer)
